% if final:
**Line Score - Final (OT)**
% else:
**Line Score**
% endif

${placeholder}
 | 1 | 2 | 3 | 4 | OT | Total
:--:|:-:|:-:|:-:|:-:|:-:|:-:|
${away_abbr} | ${team(away_score)}
${home_abbr} | ${team(home_score)}

<%def name="team(t)">\
${t['q1']} | ${t['q2']} | ${t['q3']} | ${t['q4']} | ${t['ot']} | ${t['total']} |\
</%def>