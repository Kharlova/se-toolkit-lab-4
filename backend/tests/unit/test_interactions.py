"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_includes_interaction_with_different_learner_id() -> None:
    """Test that filtering by item_id includes interactions with different learner_id."""
    interactions = [_make_log(1, 2, 1), _make_log(2, 1, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].learner_id == 2  # Different learner_id but same item_id


def test_filter_returns_multiple_matches_for_same_item_id() -> None:
    """Test that all interactions with the same item_id are returned."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 1),
        _make_log(3, 3, 1),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 3
    assert {i.id for i in result} == {1, 2, 3}


def test_filter_returns_empty_when_no_item_matches() -> None:
    """Test that filtering with a non-existent item_id returns an empty list."""
    interactions = [_make_log(1, 1, 10), _make_log(2, 2, 20)]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_with_single_element_list_matching_item_id() -> None:
    """Test filtering a single-element list where the item matches."""
    interactions = [_make_log(1, 42, 7)]
    result = _filter_by_item_id(interactions, 7)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_returns_all_when_every_interaction_has_same_item_id() -> None:
    """Test that when all interactions share the queried item_id, all are returned."""
    interactions = [
        _make_log(1, 1, 5),
        _make_log(2, 2, 5),
        _make_log(3, 3, 5),
    ]
    result = _filter_by_item_id(interactions, 5)
    assert len(result) == 3
    assert result == interactions
