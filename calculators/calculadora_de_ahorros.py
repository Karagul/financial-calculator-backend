from flask import jsonify, request

from .calculators import calculators
from utils import get_balances, get_deposits, get_periods, get_table, \
    get_table_a, get_table_m, HEADERS, parse_data


@calculators.route('/calculadora-de-ahorros', methods=['POST'])
def calculadora_de_ahorros():
    data = parse_data(request.get_json())

    ini_dep = data.get('ini_dep')
    reg_dep = data.get('reg_dep')
    freq = data.get('freq')
    num_of_years = data.get('num_of_years')
    rate = data.get('rate')
    extra_dep = data.get('extra_dep')
    extra_dep_start = data.get('extra_dep_start')
    extra_dep_f = data.get('extra_dep_f')
    dep_when = data.get('dep_when')
    time_scale, rows_per_page = data.get('time_scale')

    periods, periods_m, periods_a = get_periods(freq, num_of_years)

    deposits, reg_deps, extra_deps = get_deposits(ini_dep,
                                                  reg_dep,
                                                  extra_dep,
                                                  extra_dep_start,
                                                  extra_dep_f,
                                                  periods)

    interests, agg_interests, agg_deposits, balances = get_balances(
        periods, deposits, ini_dep, rate, freq, dep_when)

    return jsonify({
        'time_scale': time_scale,
        'total_dep': sum(deposits),
        'total_int': sum(interests),
        'fin_bal': balances[-1],
        'periods': periods,
        'agg_deposits': agg_deposits,
        'agg_interests': agg_interests,
        'balances': balances,
        'table': get_table(periods, deposits, interests, balances),
        'table_m': get_table_m(periods_m, deposits, interests, balances,
                               freq),
        'table_a': get_table_a(periods_a, deposits, interests, balances,
                               freq)
    }), 200, HEADERS
