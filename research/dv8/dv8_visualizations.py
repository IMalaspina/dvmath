"""
DV8 Visualizations
==================

Create visualizations for the numerical experiments:
1. Associator heatmap (3D cube projection)
2. STO iteration trajectory
3. Norm preservation comparison across dimensions

Author: Ivano Franco Malaspina
Date: December 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from dvmath_dv8_corrected import DV8
from dvmath_core import DV2, DV4


# Set up matplotlib for better quality
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9


def associator_norm(a, b, c):
    """Compute the norm of the associator [a, b, c]."""
    left = (a * b) * c
    right = a * (b * c)
    return (left - right).norm()


def visualize_associator_heatmap():
    """
    Visualization 1: Heatmap of associator norms for basis triplets.
    
    Since we have 7x7x7 = 343 triplets, we'll create a 2D heatmap
    by fixing the first index and showing (j, k) for each i.
    """
    print("Generating associator heatmap...")
    
    # Define basis elements
    basis = [DV8(0, 1, 0, 0, 0, 0, 0, 0),  # e1
             DV8(0, 0, 1, 0, 0, 0, 0, 0),  # e2
             DV8(0, 0, 0, 1, 0, 0, 0, 0),  # e3
             DV8(0, 0, 0, 0, 1, 0, 0, 0),  # e4
             DV8(0, 0, 0, 0, 0, 1, 0, 0),  # e5
             DV8(0, 0, 0, 0, 0, 0, 1, 0),  # e6
             DV8(0, 0, 0, 0, 0, 0, 0, 1)]  # e7
    
    # Create a figure with subplots for different fixed i values
    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    fig.suptitle('Non-Associativity Map: ||[e_i, e_j, e_k]|| for DV8', fontsize=14, fontweight='bold')
    
    axes = axes.flatten()
    
    for i in range(7):
        # Compute associator norms for this i
        heatmap_data = np.zeros((7, 7))
        for j in range(7):
            for k in range(7):
                heatmap_data[j, k] = associator_norm(basis[i], basis[j], basis[k])
        
        # Plot heatmap
        im = axes[i].imshow(heatmap_data, cmap='YlOrRd', vmin=0, vmax=2, aspect='auto')
        axes[i].set_title(f'i = e{i+1}', fontweight='bold')
        axes[i].set_xlabel('k (third element)')
        axes[i].set_ylabel('j (second element)')
        axes[i].set_xticks(range(7))
        axes[i].set_yticks(range(7))
        axes[i].set_xticklabels([f'e{x+1}' for x in range(7)])
        axes[i].set_yticklabels([f'e{y+1}' for y in range(7)])
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=axes[i], fraction=0.046, pad=0.04)
        cbar.set_label('||[a,b,c]||', rotation=270, labelpad=15)
    
    # Hide the 8th subplot
    axes[7].axis('off')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/dv8_associator_heatmap.png', bbox_inches='tight')
    print("  → Saved: dv8_associator_heatmap.png")
    plt.close()


def visualize_sto_iteration():
    """
    Visualization 2: STO iteration trajectory in 3D projection.
    
    We'll project the 8D vector onto the first 3 components for visualization.
    """
    print("Generating STO iteration trajectory...")
    
    v = DV8(1, 2, 3, 4, 5, 6, 7, 8)
    
    # Iterate STO and collect trajectory
    trajectory = [v.components[:3]]  # First 3 components for 3D plot
    norms = [v.norm()]
    current = v
    
    for _ in range(8):
        current = current.STO()
        trajectory.append(current.components[:3])
        norms.append(current.norm())
    
    trajectory = np.array(trajectory)
    
    # Create 3D plot
    fig = plt.figure(figsize=(12, 5))
    
    # 3D trajectory
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], 
             marker='o', markersize=6, linewidth=2, color='steelblue', alpha=0.7)
    ax1.scatter(trajectory[0, 0], trajectory[0, 1], trajectory[0, 2], 
                color='green', s=100, marker='*', label='Start', zorder=10)
    ax1.scatter(trajectory[-1, 0], trajectory[-1, 1], trajectory[-1, 2], 
                color='red', s=100, marker='X', label='End (= Start)', zorder=10)
    
    # Annotate points
    for i in range(len(trajectory)):
        ax1.text(trajectory[i, 0], trajectory[i, 1], trajectory[i, 2], 
                 f'  {i}', fontsize=8)
    
    ax1.set_xlabel('Component 1 (v)', fontweight='bold')
    ax1.set_ylabel('Component 2 (d₁)', fontweight='bold')
    ax1.set_zlabel('Component 3 (d₂)', fontweight='bold')
    ax1.set_title('STO Iteration Trajectory (3D Projection)', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Norm preservation plot
    ax2 = fig.add_subplot(122)
    ax2.plot(range(len(norms)), norms, marker='o', markersize=8, 
             linewidth=2, color='darkgreen', label='||STO^n(v)||')
    ax2.axhline(y=norms[0], color='red', linestyle='--', linewidth=1.5, 
                label=f'Original norm = {norms[0]:.4f}')
    ax2.set_xlabel('Iteration n', fontweight='bold')
    ax2.set_ylabel('Norm', fontweight='bold')
    ax2.set_title('Norm Preservation in STO Iteration', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xticks(range(len(norms)))
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/dv8_sto_iteration.png', bbox_inches='tight')
    print("  → Saved: dv8_sto_iteration.png")
    plt.close()


def visualize_dimension_comparison():
    """
    Visualization 3: Comparison of properties across DV2, DV4, DV8.
    """
    print("Generating dimension comparison chart...")
    
    # Test norm preservation with random vectors
    np.random.seed(42)
    n_tests = 100
    
    dv2_errors = []
    dv4_errors = []
    dv8_errors = []
    
    for _ in range(n_tests):
        # DV2
        a2 = DV2(*np.random.randn(2))
        b2 = DV2(*np.random.randn(2))
        expected2 = a2.norm() * b2.norm()
        actual2 = (a2 * b2).norm()
        dv2_errors.append(abs(expected2 - actual2))
        
        # DV4
        a4 = DV4(*np.random.randn(4))
        b4 = DV4(*np.random.randn(4))
        expected4 = a4.norm() * b4.norm()
        actual4 = (a4 * b4).norm()
        dv4_errors.append(abs(expected4 - actual4))
        
        # DV8
        a8 = DV8(*np.random.randn(8))
        b8 = DV8(*np.random.randn(8))
        expected8 = a8.norm() * b8.norm()
        actual8 = (a8 * b8).norm()
        dv8_errors.append(abs(expected8 - actual8))
    
    # Create comparison plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Error distribution
    ax1 = axes[0]
    ax1.hist(dv2_errors, bins=20, alpha=0.6, label='DV2 (ℂ)', color='blue', edgecolor='black')
    ax1.hist(dv4_errors, bins=20, alpha=0.6, label='DV4 (ℍ)', color='orange', edgecolor='black')
    ax1.hist(dv8_errors, bins=20, alpha=0.6, label='DV8 (𝕆)', color='green', edgecolor='black')
    ax1.set_xlabel('Norm Preservation Error |expected - actual|', fontweight='bold')
    ax1.set_ylabel('Frequency', fontweight='bold')
    ax1.set_title('Norm Preservation Accuracy (100 random tests)', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_yscale('log')
    
    # Property summary bar chart
    ax2 = axes[1]
    properties = ['Commutative', 'Associative', 'Norm-\nPreserving', 'STO Norm-\nPreserving']
    dv2_props = [1, 1, 1, 1]
    dv4_props = [0, 1, 1, 1]
    dv8_props = [0, 0, 1, 1]
    
    x = np.arange(len(properties))
    width = 0.25
    
    ax2.bar(x - width, dv2_props, width, label='DV2 (ℂ)', color='blue', alpha=0.7)
    ax2.bar(x, dv4_props, width, label='DV4 (ℍ)', color='orange', alpha=0.7)
    ax2.bar(x + width, dv8_props, width, label='DV8 (𝕆)', color='green', alpha=0.7)
    
    ax2.set_ylabel('Property Satisfied (1 = Yes, 0 = No)', fontweight='bold')
    ax2.set_title('Algebraic Properties Across Dimensions', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(properties)
    ax2.legend()
    ax2.set_ylim([0, 1.2])
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add annotations
    for i, (p2, p4, p8) in enumerate(zip(dv2_props, dv4_props, dv8_props)):
        ax2.text(i - width, p2 + 0.05, '✓' if p2 else '✗', ha='center', fontsize=12, fontweight='bold')
        ax2.text(i, p4 + 0.05, '✓' if p4 else '✗', ha='center', fontsize=12, fontweight='bold')
        ax2.text(i + width, p8 + 0.05, '✓' if p8 else '✗', ha='center', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/dv8_dimension_comparison.png', bbox_inches='tight')
    print("  → Saved: dv8_dimension_comparison.png")
    plt.close()


def visualize_associator_distribution():
    """
    Visualization 4: Distribution of associator norms.
    """
    print("Generating associator distribution...")
    
    # Define basis elements
    basis = [DV8(0, 1, 0, 0, 0, 0, 0, 0),  # e1
             DV8(0, 0, 1, 0, 0, 0, 0, 0),  # e2
             DV8(0, 0, 0, 1, 0, 0, 0, 0),  # e3
             DV8(0, 0, 0, 0, 1, 0, 0, 0),  # e4
             DV8(0, 0, 0, 0, 0, 1, 0, 0),  # e5
             DV8(0, 0, 0, 0, 0, 0, 1, 0),  # e6
             DV8(0, 0, 0, 0, 0, 0, 0, 1)]  # e7
    
    # Compute all associator norms
    norms = []
    for i in range(7):
        for j in range(7):
            for k in range(7):
                norm = associator_norm(basis[i], basis[j], basis[k])
                norms.append(norm)
    
    norms = np.array(norms)
    
    # Create distribution plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    ax1 = axes[0]
    counts, bins, patches = ax1.hist(norms, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
    ax1.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Associative (norm = 0)')
    ax1.set_xlabel('Associator Norm ||[e_i, e_j, e_k]||', fontweight='bold')
    ax1.set_ylabel('Frequency', fontweight='bold')
    ax1.set_title('Distribution of Associator Norms (343 triplets)', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add statistics
    zero_count = np.sum(norms < 1e-9)
    non_zero_count = len(norms) - zero_count
    ax1.text(0.98, 0.98, f'Associative: {zero_count} ({100*zero_count/len(norms):.1f}%)\n'
                          f'Non-associative: {non_zero_count} ({100*non_zero_count/len(norms):.1f}%)',
             transform=ax1.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Pie chart
    ax2 = axes[1]
    sizes = [zero_count, non_zero_count]
    labels = [f'Associative\n({zero_count} triplets)', f'Non-Associative\n({non_zero_count} triplets)']
    colors = ['lightcoral', 'lightgreen']
    explode = (0.05, 0)
    
    ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title('Associativity vs Non-Associativity in DV8', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/dv8_associator_distribution.png', bbox_inches='tight')
    print("  → Saved: dv8_associator_distribution.png")
    plt.close()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Generating DV8 Visualizations")
    print("=" * 70 + "\n")
    
    visualize_associator_heatmap()
    visualize_sto_iteration()
    visualize_dimension_comparison()
    visualize_associator_distribution()
    
    print("\n" + "=" * 70)
    print("All visualizations generated successfully!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  1. dv8_associator_heatmap.png")
    print("  2. dv8_sto_iteration.png")
    print("  3. dv8_dimension_comparison.png")
    print("  4. dv8_associator_distribution.png")
    print("=" * 70)
