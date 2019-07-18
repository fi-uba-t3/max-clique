from hypothesis import given
import hypothesis.strategies as st

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from triangles import Triangles

@st.composite
def triangles_visited_pair(draw):

    n = draw(st.integers( min_value=2, max_value=400))
    triangles_list = st.lists(st.integers(min_value=0, max_value=n - 2), min_size=n, max_size=n)
    visited_map = st.lists(st.booleans(), min_size=n, max_size=n)
    return (draw(triangles_list), draw(visited_map))

@given(triangles_visited_pair())
def test_triangles_always_decreasing(triangles_visited_pair):
    triangles_list, visited_map = triangles_visited_pair
    index = 0
    t = Triangles(visited_map)
    for triangles in triangles_list:
        t.add(index, triangles)
        index += 1

    previous_value = 9000000000000
    for max_clique_size, index in t.get_t_n_iterator():
        assert max_clique_size <= previous_value # Always decreases
        assert max_clique_size <= len(triangles_list) # Always lower than the amount of nodes
        previous_value = max_clique_size

test_triangles_always_decreasing()
