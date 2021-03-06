import os

ticker_delay_in_seconds = 4
averaged_price_time_span_in_seconds = 60
maximum_elements_in_price_history = 1440
price_logging_period_in_minutes = 60
minimum_interesting_difference_in_percentage = 0.5
anteriorities_in_minutes = [1, 5, 10, 15, 30, 60, 180, 360, 1440]
pairs_to_watch = ['XXBTZEUR', 'XETHZEUR', 'XXMRZEUR', 'XLTCZEUR', 'XXRPZEUR', 'DASHEUR', 'BCHEUR']
fee_percentage = 0.26
base_trade_amount_in_euros = 10.00
trading_risk_level = int(os.environ.get('RISK_LEVEL') or 0)
