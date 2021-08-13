[](/${away_abbr})${away_abbr} | [](/${home_abbr})${home_abbr}
:---|:---
% for r in rosters:
${player(r['away'])} | ${player(r['home'])}
% endfor

<%def name="player(p)">${p['uniform']} ${p['first_name']} ${p['last_name']}</%def>