from django.shortcuts import render
from django.db.models import Sum, Value, DecimalField, F
from django.db.models.functions import Coalesce, TruncDay, TruncMonth
from django.utils.timezone import now
import json
from decimal import Decimal
from payments.models import DuePayment, CustomerPayment
from expense.models import Expense
from customer.models import Customer
from sell.models import Sell
from buy.models import AddStock, Stock
from vendor.models import Vendor

# payments optional
try:
    from payments.models import Payment
except Exception:
    Payment = None


def _has_field(model, field_name):
    return any(f.name == field_name for f in model._meta.get_fields())


def _coalesce_sum(qs, field):
    return float(qs.aggregate(total=Coalesce(Sum(field, output_field=DecimalField()), Value(0, output_field=DecimalField())))['total'] or 0)


def _timeseries(qs, date_field_name, value_field, trunc_func):
    qs = qs.annotate(period=trunc_func(date_field_name)).values('period').annotate(
        total=Coalesce(Sum(value_field, output_field=DecimalField()), Value(0, output_field=DecimalField()))
    ).order_by('period')
    out = []
    for e in qs:
        period = e['period']
        s = period.isoformat() if hasattr(period, 'isoformat') else str(period)
        out.append({'day': s, 'total': float(e['total'])})
    return out


def dashboard_view(request):
    # choose date field (common names: 'date' or 'reserve_date')
    date_field = 'date' if _has_field(Sell, 'date') else ('reserve_date' if _has_field(Sell, 'reserve_date') else 'date')

    # filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    month = request.GET.get('month')  # YYYY-MM
    year = request.GET.get('year')

    # base querysets
    sales_qs = Sell.objects.all().order_by('date' if _has_field(Sell, 'date') else 'reserve_date')
    expenses_qs = Expense.objects.all().order_by('date' if _has_field(Expense, 'date') else 'id')

    # apply date filters
    if start_date and end_date:
        sales_qs = sales_qs.filter(**{f"{date_field}__range": [start_date, end_date]})
        expenses_qs = expenses_qs.filter(date__range=[start_date, end_date])
    elif month:
        try:
            yyyy, mm = month.split('-')
            sales_qs = sales_qs.filter(**{f"{date_field}__year": int(yyyy), f"{date_field}__month": int(mm)})
            expenses_qs = expenses_qs.filter(date__year=int(yyyy), date__month=int(mm))
        except Exception:
            pass
    elif year:
        try:
            y = int(year)
            sales_qs = sales_qs.filter(**{f"{date_field}__year": y})
            expenses_qs = expenses_qs.filter(date__year=y)
        except Exception:
            pass
    else:
        now_dt = now()
        sales_qs = sales_qs.filter(**{f"{date_field}__year": now_dt.year, f"{date_field}__month": now_dt.month})
        expenses_qs = expenses_qs.filter(date__year=now_dt.year, date__month=now_dt.month)

    # Totals (safe with Coalesce + DecimalField)
    total_sales = _coalesce_sum(sales_qs, 'total_amount')
    total_expenses = _coalesce_sum(expenses_qs, 'amount')
    total_profit = total_sales - total_expenses

    # Cylinders sold totals (handle possible field names)
    dom_field = 'no_domestic_cylinder' if _has_field(Sell, 'no_domestic_cylinder') else ('domestic_qty' if _has_field(Sell, 'domestic_qty') else None)
    com_field = 'no_commercial_cylinder' if _has_field(Sell, 'no_commercial_cylinder') else ('commercial_qty' if _has_field(Sell, 'commercial_qty') else None)
    cylinders_sold = 0
    if dom_field and com_field:
        dom = _coalesce_sum(sales_qs, dom_field)
        com = _coalesce_sum(sales_qs, com_field)
        cylinders_sold = int(dom + com)
    else:
        # fallback: try single field 'quantity' or zero
        if _has_field(Sell, 'quantity'):
            cylinders_sold = int(_coalesce_sum(sales_qs, 'quantity'))
        else:
            cylinders_sold = 0

    # Stock current and previous month
    current_month_stock = AddStock.objects.filter(date__month=now().month).aggregate(
        domestic=Coalesce(Sum('no_domestic_cylinder', output_field=DecimalField()), Value(0, output_field=DecimalField())),
        commercial=Coalesce(Sum('no_commercial_cylinder', output_field=DecimalField()), Value(0, output_field=DecimalField()))
    )
    
    previous_month_stock = AddStock.objects.filter(date__month=now().month - 1).aggregate(
        domestic=Coalesce(Sum('no_domestic_cylinder', output_field=DecimalField()), Value(0, output_field=DecimalField())),
        commercial=Coalesce(Sum('no_commercial_cylinder', output_field=DecimalField()), Value(0, output_field=DecimalField()))
    )

    stock_current = [float(current_month_stock['domestic']), float(current_month_stock['commercial'])]
    stock_previous = [float(previous_month_stock['domestic']), float(previous_month_stock['commercial'])]

    # Recent lists
    recent_sales = sales_qs.order_by(f"-{date_field}")[:5]
    recent_purchases = expenses_qs.order_by("-date")[:5]

    # Timeseries for charts (day-based)
    sales_day = _timeseries(Sell.objects.all(), date_field, 'total_amount', TruncDay)
    expenses_day = _timeseries(AddStock.objects.all(), 'date', 'total_amount', TruncDay)

    # Profit per day = sales - expenses (merge by day)
    def _merge_profit(sales_ts, exp_ts):
        s_map = {e['day']: e['total'] for e in sales_ts}
        e_map = {e['day']: e['total'] for e in exp_ts}
        labels = sorted(set(s_map.keys()) | set(e_map.keys()))
        out = []
        for lbl in labels:
            out.append({'day': lbl, 'profit': float(Decimal(s_map.get(lbl, 0)) - Decimal(e_map.get(lbl, 0)))})
        return out

    profit_day = _merge_profit(sales_day, expenses_day)

    # Cylinders timeseries (per day)
    def _cylinders_ts(qs, date_field_name, dom_field_name, com_field_name):
        if not dom_field_name or not com_field_name:
            return []
        qs2 = qs.annotate(period=TruncDay(date_field_name)).values('period').annotate(
            dom=Coalesce(Sum(dom_field_name, output_field=DecimalField()), Value(0, output_field=DecimalField())),
            com=Coalesce(Sum(com_field_name, output_field=DecimalField()), Value(0, output_field=DecimalField()))
        ).order_by('period')
        out = []
        for e in qs2:
            p = e['period']
            out.append({'day': p.isoformat() if hasattr(p, 'isoformat') else str(p), 'total': int(e['dom'] + e['com'])})
        return out

    cylinders_day = _cylinders_ts(Sell.objects.all(), date_field, dom_field, com_field)

    
    current_stock = Stock.objects.first()
   
    # Prepare JSON payloads for template
    context = {
        'customers_count': Customer.objects.count(),
        'vendors_count': Vendor.objects.count(),
        'sales_count': Sell.objects.count(),
        'purchases_count': AddStock.objects.count(),
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'total_profit': total_profit,
        'cylinders_sold': cylinders_sold,
        'domestic_in_stock': int(current_stock.no_domestic_cylinder) if current_stock else 0,
        'commercial_in_stock': int(current_stock.no_commercial_cylinder) if current_stock else 0,
        'recent_sales': recent_sales,
        'recent_purchases': recent_purchases,
        'sales_day': json.dumps(sales_day),
        'expenses_day': json.dumps(expenses_day),
        'profit_day': json.dumps(profit_day),
        'cylinders_day': json.dumps(cylinders_day),
        'stock_current': json.dumps(stock_current),
        'stock_previous': json.dumps(stock_previous),
    }

    return render(request, 'dashboard/dashboard.html', context)