"""
Sprint 3 - Day 19
Radar Chart Generator
"""

import matplotlib.pyplot as plt
import numpy as np
def create_radar(company_name, values, labels, output_file):
    """
    Generate a radar chart for one company.
    """

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    )

    values = np.concatenate(
        (values, [values[0]])
    )

    angles = np.concatenate(
        (angles, [angles[0]])
    )

    fig = plt.figure(figsize=(6, 6))

    ax = fig.add_subplot(
        111,
        polar=True
    )

    ax.plot(angles, values)

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(labels)

    ax.set_title(company_name)

    plt.savefig(output_file)

    plt.close()