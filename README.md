<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>

<h1>Puzzle Game Suite</h1>

<h2>Overview</h2>
<p>This repository showcases a suite of puzzle games designed to demonstrate various machine learning principles in a practical, interactive environment. Each game in the suite — Tile Puzzle, Grid Navigation, and Dominoes Game — is accompanied by a graphical user interface (GUI) for enhanced playability. The Tile Puzzle utilizes search algorithms to solve the puzzle from any given state, demonstrating depth-first and A* search strategies. Grid Navigation employs heuristic search to navigate efficiently through a grid with obstacles, a fundamental technique in pathfinding and AI. The Dominoes Game illustrates decision-making under uncertainty, adversarial search, and the minimax algorithm with alpha-beta pruning, foundational concepts in game theory and strategic AI.</p>

<h2>Setup</h2>
<p>No special setup is required beyond having Python installed on your system. The games are written in Python 3.6+ using standard libraries.</p>

<h2>Running the Games</h2>
<p>To enjoy the games, navigate to the <code>gui</code> directory and run the following commands:</p>

<p>For Tile Puzzle:</p>
<pre><code>python gui/tile_puzzle_gui.py rows cols</code></pre>

<p>For Grid Navigation:</p>
<pre><code>python gui/grid_navigation_gui.py scene_path</code></pre>

<p>For Dominoes Game:</p>
<pre><code>python gui/dominoes_game_gui.py rows cols</code></pre>

<p>Each command launches the GUI for the respective puzzle game, allowing for interactive play and exploration of the underlying machine learning algorithms.</p>

<h2>Testing</h2>
<p>A comprehensive test suite is provided to verify the functionality of the puzzle games. To run the tests, execute the following command from the root directory of the project:</p>

<pre><code>python -m unittest discover tests</code></pre>

<p>This command will find and run all test cases within the <code>tests</code> directory, ensuring that each component of the puzzle suite operates as expected.</p>

</body>
</html
