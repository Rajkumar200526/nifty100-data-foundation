from pathlib import Path


def test_cluster_labels_exists():
    assert Path("output/cluster_labels.csv").exists()


def test_outlier_report_exists():
    assert Path("output/outlier_report.csv").exists()


def test_portfolio_statistics_exists():
    assert Path("output/portfolio_statistics.csv").exists()


def test_elbow_plot_exists():
    assert Path("reports/elbow_plot.png").exists()


def test_heatmap_exists():
    assert Path("reports/correlation_heatmap.png").exists()