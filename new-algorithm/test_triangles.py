from hypothesis import given
import hypothesis.strategies as st
from triangles import Triangles


@given(
  st.lists(st.integers(min_value=0, max_value=400), min_size=0, max_size=40000),
  )
def test_triangles_always_decreasing(triangles_list):
    index = 0
    t = Triangles()
    for triangles in triangles_list:
        t.add(index, triangles)
        index += 1

    previous_value = 9000000000000
    for max_clique_size, index in t.get_t_n_iterator():
        assert max_clique_size <= previous_value
        print(max_clique_size)
        assert max_clique_size <= len(triangles_list)
        previous_value = max_clique_size



test_triangles_always_decreasing()