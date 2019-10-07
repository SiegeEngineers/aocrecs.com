"""Match participants."""
import networkx


def compute_participants(matches, challonge_data):
    """Compute series participants.

    Iterate all matches and players to create a graph.
    Apply connected components algorithm to resolve distinct
    participant groups over all matches.

    Sort participant groups by number of wins to correlate
    with Challonge participant data (which also includes number
    of wins).

    Note that edge cases exist that are not covered. For example,
    teams sometimes field a 1v1 player for a single match. If neither
    player in the 1v1 match takes part in any other matches,
    the players can't be placed in a participant group and their win
    is not counted. There are two consequences:

    1. Not counting a win may make the number of wins between
       participants even, in which case we don't know which
       participant group won the series.
    2. Not grouping a player means the participant player list
       will be incomplete.
    """
    graph = networkx.DiGraph()
    win_id = 0
    for match in matches:
        # Record a win
        win_id += 1
        graph.add_node(win_id, type='win')

        # Add node for each player
        for player in match.players:
            graph.add_node(player.user_id, type='player')

        # Connect winning players to recorded win
        for player in match.winning_team:
            graph.add_edge(player.user_id, win_id)

        # Connect all players on the same team
        for team in match.teams:
            for i in team.members:
                for j in team.members:
                    graph.add_edge(i.user_id, j.user_id)

    mgz_data = [{
        'wins': len([node for node in g if graph.node[node]['type'] == 'win']),
        'players': [node for node in g if graph.node[node]['type'] == 'player']
    } for g in networkx.weakly_connected_components(graph)]

    return [{
        'user_ids': mgz['players'],
        'winner': challonge.winner,
        'name': challonge.name,
        'score': challonge.score
    } for mgz, challonge in zip(
        sorted(mgz_data, key=lambda k: -1 * k['wins']),
        sorted(challonge_data, key=lambda k: -1 * k.score)
    )]
