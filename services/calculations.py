def allowance_excess(ewa, ac, allowance):
    return max((ewa + ac) - allowance, 0)

def roi(total_income, total_spending, cost):
    return ((total_income - total_spending) / cost) * 100
