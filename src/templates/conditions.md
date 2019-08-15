${placeholder}
Sky | Temp | Wind | Field | Coin Toss
:---|:----:|:----:|:-----:|:--------
${weather['sky']} | ${weather['temperature']}C | ${weather['wind_direction']} ${weather['wind_speed']} | ${weather['field_conditions']} | ${cointoss(coin_toss)}

<%def name="cointoss(x)">
% if x['coin_toss_winner'] != '':
${x['coin_toss_winner_election']}\
% endif
</%def>