Quarter | Time | Play | [](/${away_abbr})${away_abbr} | [](/${home_abbr})${home_abbr}
:---:|:---:|:---|:---:|:---:\
% for p in plays:
${play(p)}\
% endfor

<%def name="play(p)">
${p['qtr']} | ${p['time']} | ${p['play']} | ${p['away_score']} | ${p['home_score']}\
</%def>