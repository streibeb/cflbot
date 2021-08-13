 | 1 | 2 | 3 | 4 | Total
:--:|:-:|:-:|:-:|:-:|:-:|\
% for t in teams:
${team(t)}\
% endfor

<%def name="team(t)">
[](/${t['abbr']})${t['abbr']} | ${t['q1']} | ${t['q2']} | ${t['q3']} | ${t['q4']} | ${t['total']} |\
</%def>