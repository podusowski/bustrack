from utils import contains_segment, same_place, extract_segments


# distance between two meridians on equator is something close to 111km
MERIDIANS_DISTANCE_ON_EQUATOR=150000


def test_same_place_one_dim():
    assert same_place(1, 1, sensitivity=0)
    assert not same_place(1, 2, sensitivity=0)
    assert same_place(1, 2, sensitivity=MERIDIANS_DISTANCE_ON_EQUATOR)


_ROUTE_GOING_RIGHT = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]


def test_empty_route_doesnt_have_any_segments():
    assert not contains_segment([], [(0, 0)])


def test_route_contains_segment_that_is_equal():
    assert contains_segment(_ROUTE_GOING_RIGHT, _ROUTE_GOING_RIGHT)


def test_route_contains_segment_that_starts_the_same():
    assert contains_segment(_ROUTE_GOING_RIGHT, _ROUTE_GOING_RIGHT[0:3])


def test_route_contains_segment_that_ends_the_same():
    assert contains_segment(_ROUTE_GOING_RIGHT, _ROUTE_GOING_RIGHT[:-3])


def test_segment_is_in_the_middle():
    assert contains_segment([1, 2, 3, 4, 5], [2, 4])


def test_segment_is_in_the_middle_but_with_some_offset():
    assert contains_segment([10, 20, 30, 40, 50], [21, 41], sensitivity=MERIDIANS_DISTANCE_ON_EQUATOR)


def test_totally_different_segment():
    assert not contains_segment([1, 2, 3, 4, 5], [4, 2])


def test_route_doesnt_contain_segment():
    assert not contains_segment(_ROUTE_GOING_RIGHT, [(0, 1), (0, 2)])


# extract segments


SEGMENT_TWO_POINTS_RIGTH = [(0, 0), (1, 0)]
SEGMENT_TEN_POINTS_RIGTH = [(x, 0) for x in range(10)]


def test_extract_no_segments_from_empty_record():
    assert [] == list(extract_segments([], [SEGMENT_TWO_POINTS_RIGTH]))


def test_segment_matching_record_exactly():
    assert [SEGMENT_TWO_POINTS_RIGTH] == list(extract_segments(SEGMENT_TWO_POINTS_RIGTH, [SEGMENT_TWO_POINTS_RIGTH]))


def test_segment_matching_records_beginning():
    assert [SEGMENT_TEN_POINTS_RIGTH[:3]] == list(extract_segments(SEGMENT_TEN_POINTS_RIGTH, [SEGMENT_TEN_POINTS_RIGTH[:3]]))


def test_segment_matching_records_end():
    assert [SEGMENT_TEN_POINTS_RIGTH[3:]] == list(extract_segments(SEGMENT_TEN_POINTS_RIGTH, [SEGMENT_TEN_POINTS_RIGTH[3:]]))


def test_segment_matching_records_middle():
    assert [SEGMENT_TEN_POINTS_RIGTH[3:6]] == list(extract_segments(SEGMENT_TEN_POINTS_RIGTH, [SEGMENT_TEN_POINTS_RIGTH[3:6]]))


def test_segment_matching_records_twice():
    segment = SEGMENT_TEN_POINTS_RIGTH[:3]
    record = SEGMENT_TEN_POINTS_RIGTH + SEGMENT_TEN_POINTS_RIGTH
    assert [segment, segment] == list(extract_segments(record, [segment]))


def test_strided_segment_matching():
    segment = SEGMENT_TEN_POINTS_RIGTH[3:6:2]
    record = SEGMENT_TEN_POINTS_RIGTH
    assert [segment] == list(extract_segments(record, [segment]))


def test_different_segment_doesnt_match():
    assert [] == list(extract_segments(SEGMENT_TEN_POINTS_RIGTH, [(20, 0), (20, 0)]))