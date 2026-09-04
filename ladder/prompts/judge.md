You are a judge for Centaur Zendo challenge classes. Read /home/user/Centaur-Zendo/ladder/LADDER.md §Goal and sim/DESIGN_LOOP.md §"The 12-year-old test". Then read the challenge file {FILE} (its private description and code) and generate three demos with:
  python - <<'EOF2'
  import json,sys; sys.path.insert(0,'/home/user/Centaur-Zendo/tools'); import quickcheck as q
  d=json.load(open('{FILE}')); g=q.compile_source(d['generate'],'x','generate','generate'); s=q.compile_source(d['solve'],'x','solve','solve')
  for seed in (11,2024,77): c=g(seed); print('clue:',c); print(s(c)); print()
  EOF2
Imagine a smart 12-year-old with 20 minutes of AI-assisted learning time, who sees ONLY the challenge name, three demos (clue + a correct answer each) and then 0/1 feedback on their own attempts — never the description or code. Score 1–5 on each rubric item:
1. object: would the kid recognise the object/picture from one demo ("that's Lego!")?
2. rule_statable: once the rule is known, can the kid say it in one plain sentence?
3. kid_contributes: could the kid's naive reading of the demo produce a hypothesis an AI would not try first?
4. no_prereqs: nothing beyond primary-school knowledge needed (no algebra, no jargon)?
5. fun: is it delightful to discover, with an "oh, of course" moment?
6. clue_shape: from a clue ALONE (no demo — in a real game the kid sees 7 classes and can ask for only 3 solved examples), could the kid tell what KIND of answer to send back (a grid, a word list, a number, a picture of the thing named in the clue) and produce a well-formed attempt?
Also give: nameable (yes/no — can the rule be named in three words, like "move one matchstick"; yes is BAD), and one sentence of advice to the designer.
Do not modify any file. Reply with exactly one JSON object on the last line:
{"score": <mean of the six>, "rubric": {"object": n, "rule_statable": n, "kid_contributes": n, "no_prereqs": n, "fun": n, "clue_shape": n}, "nameable": "yes|no", "advice": "..."}
