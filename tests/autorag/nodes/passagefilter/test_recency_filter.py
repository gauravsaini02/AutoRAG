from autorag.nodes.passagefilter import recency_filter

from tests.autorag.nodes.passagefilter.test_passage_filter_base import contents_example, time_list, ids_example, \
    scores_example, base_passage_filter_test, base_passage_filter_node_test, project_dir_with_corpus, \
    previous_result


def test_recency_filter():
    original_recency_filter = recency_filter.__wrapped__
    contents_result, id_result, score_result = original_recency_filter \
        (contents_example, scores_example, ids_example, time_list, threshold="2021-06-30")
    assert id_result[0] == [ids_example[0][1], ids_example[0][2], ids_example[0][3]]
    assert id_result[1] == [ids_example[1][2], ids_example[1][3]]
    assert contents_result[0] == [contents_example[0][1], contents_example[0][2], contents_example[0][3]]
    assert contents_result[1] == [contents_example[1][2], contents_example[1][3]]
    assert score_result[0] == [0.8, 0.1, 0.5]
    assert score_result[1] == [0.7, 0.3]
    base_passage_filter_test(contents_result, id_result, score_result)


def test_recency_filter_all_filtered():
    original_recency_filter = recency_filter.__wrapped__
    contents_result, id_result, score_result = original_recency_filter \
        (contents_example, scores_example, ids_example, time_list, threshold="2040-06-30")
    assert id_result[0] == [ids_example[0][3]]
    assert id_result[1] == [ids_example[1][3]]
    assert contents_result[0] == [contents_example[0][3]]
    assert contents_result[1] == [contents_example[1][3]]
    assert score_result[0] == [0.5]
    assert score_result[1] == [0.3]
    base_passage_filter_test(contents_result, id_result, score_result)


def test_recency_filter_wrong_threshold():
    original_recency_filter = recency_filter.__wrapped__
    contents_result, id_result, score_result = original_recency_filter \
        (contents_example, scores_example, ids_example, time_list, threshold="havertz")
    assert id_result[0] == ids_example[0]
    assert id_result[1] == ids_example[1]
    assert contents_result[0] == contents_example[0]
    assert contents_result[1] == contents_example[1]
    assert score_result[0] == scores_example[0]
    assert score_result[1] == scores_example[1]
    base_passage_filter_test(contents_result, id_result, score_result)


def test_recency_filter_minutes():
    original_recency_filter = recency_filter.__wrapped__
    contents_result, id_result, score_result = original_recency_filter \
        (contents_example, scores_example, ids_example, time_list, threshold="2022-03-05 12:35")
    assert id_result[0] == [ids_example[0][3]]
    assert id_result[1] == [ids_example[1][2], ids_example[1][3]]
    assert contents_result[0] == [contents_example[0][3]]
    assert contents_result[1] == [contents_example[1][2], contents_example[1][3]]
    assert score_result[0] == [0.5]
    assert score_result[1] == [0.7, 0.3]
    base_passage_filter_test(contents_result, id_result, score_result)


def test_recency_filter_seconds():
    original_recency_filter = recency_filter.__wrapped__
    contents_result, id_result, score_result = original_recency_filter \
        (contents_example, scores_example, ids_example, time_list, threshold="2022-03-05 12:40:30")
    assert id_result[0] == [ids_example[0][3]]
    assert id_result[1] == [ids_example[1][3]]
    assert contents_result[0] == [contents_example[0][3]]
    assert contents_result[1] == [contents_example[1][3]]
    assert score_result[0] == [0.5]
    assert score_result[1] == [0.3]
    base_passage_filter_test(contents_result, id_result, score_result)


def test_recency_filter_node(project_dir_with_corpus):
    result_df = recency_filter(
        project_dir=project_dir_with_corpus, previous_result=previous_result, threshold="2021-06-30")
    base_passage_filter_node_test(result_df)
