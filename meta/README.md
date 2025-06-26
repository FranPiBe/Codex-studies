# Meta

This folder is a playground for refining prompts used with OpenAI Codex. The `evaluate_prompts.py` script lets you benchmark different prompts automatically.

## How it works

1. Add your prompts to **prompts.txt**, one per line.
2. Run `python evaluate_prompts.py` from this directory.
3. The script asks Codex to solve a predefined task with each prompt, checks the generated code, and assigns a score.
4. Top responses are saved in the `results/` folder along with a leaderboard.

## Interpreting the leaderboard

Higher scores indicate that the generated code compiled, passed the functional test, and remained concise. Use the ranking to see which prompts produce the best results for the target task.

## Contributing

Feel free to extend the evaluation heuristics or provide new prompts. Pull requests that add alternative scoring methods or commentary on why certain prompts work well are welcome.
