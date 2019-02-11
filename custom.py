from __future__ import division

from math import sqrt

import networkx as nx
from networkx.utils import not_implemented_for

def custom_centrality(G, max_iter=1000, tol=1.0e-6, nstart=None,
                           weight=None):
    r"""Compute the eigenvector centrality for the graph `G`.

    Eigenvector centrality computes the centrality for a node based on the
    centrality of its neighbors. The eigenvector centrality for node $i$ is
    the $i$-th element of the vector $x$ defined by the equation

    .. math::

        Ax = \lambda x

    where $A$ is the adjacency matrix of the graph `G` with eigenvalue
    $\lambda$. By virtue of the Perron–Frobenius theorem, there is a unique
    solution $x$, all of whose entries are positive, if $\lambda$ is the
    largest eigenvalue of the adjacency matrix $A$ ([2]_).

    Parameters
    ----------
    G : graph
      A networkx graph

    max_iter : integer, optional (default=100)
      Maximum number of iterations in power method.

    tol : float, optional (default=1.0e-6)
      Error tolerance used to check convergence in power method iteration.

    nstart : dictionary, optional (default=None)
      Starting value of eigenvector iteration for each node.

    weight : None or string, optional (default=None)
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.

    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with eigenvector centrality as the value.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> centrality = nx.eigenvector_centrality(G)
    >>> sorted((v, '{:0.2f}'.format(c)) for v, c in centrality.items())
    [(0, '0.37'), (1, '0.60'), (2, '0.60'), (3, '0.37')]

    Raises
    ------
    NetworkXPointlessConcept
        If the graph `G` is the null graph.

    NetworkXError
        If each value in `nstart` is zero.

    PowerIterationFailedConvergence
        If the algorithm fails to converge to the specified tolerance
        within the specified number of iterations of the power iteration
        method.

    See Also
    --------
    eigenvector_centrality_numpy
    pagerank
    hits

    Notes
    -----
    The measure was introduced by [1]_ and is discussed in [2]_.

    The power iteration method is used to compute the eigenvector and
    convergence is **not** guaranteed. Our method stops after ``max_iter``
    iterations or when the change in the computed vector between two
    iterations is smaller than an error tolerance of
    ``G.number_of_nodes() * tol``. This implementation uses ($A + I$)
    rather than the adjacency matrix $A$ because it shifts the spectrum
    to enable discerning the correct eigenvector even for networks with
    multiple dominant eigenvalues.

    For directed graphs this is "left" eigenvector centrality which corresponds
    to the in-edges in the graph. For out-edges eigenvector centrality
    first reverse the graph with ``G.reverse()``.

    References
    ----------
    .. [1] Phillip Bonacich.
       "Power and Centrality: A Family of Measures."
       *American Journal of Sociology* 92(5):1170–1182, 1986
       <http://www.leonidzhukov.net/hse/2014/socialnetworks/papers/Bonacich-Centrality.pdf>
    .. [2] Mark E. J. Newman.
       *Networks: An Introduction.*
       Oxford University Press, USA, 2010, pp. 169.

    """
    if len(G) == 0:
        raise nx.NetworkXPointlessConcept('cannot compute centrality for the'
                                          ' null graph')
    # If no initial vector is provided, start with the all-ones vector.
    if nstart is None:
        nstart = {v: 1 for v in G}
    if all(v == 0 for v in nstart.values()):
        raise nx.NetworkXError('initial vector cannot have all zero values')
    # Normalize the initial vector so that each entry is in [0, 1]. This is
    # guaranteed to never have a divide-by-zero error by the previous line.
    x = {k: v / sum(nstart.values()) for k, v in nstart.items()}
    y = {k: v / sum(nstart.values()) for k, v in nstart.items()}

    nnodes = G.number_of_nodes()
    # make up to max_iter iterations
    for i in range(max_iter):
        print(i+1)
        xlast = x
        x = xlast.copy()  # Start with xlast times I to iterate with (A+I)
        ylast = y
        y = ylast.copy()  # Start with xlast times I to iterate with (A+I)

        # do the multiplication y^T = x^T A (left eigenvector)
        for xj in x:
            for nbr in G[xj]:
                y[nbr] += xlast[xj] * G[xj][nbr].get(weight, 1)
                x[xj]  += ylast[nbr] * G[xj][nbr].get(weight, 1)
        # for yj in y:
        #     for nbr in G[yj]:
        #         x[nbr] += ylast[yj] * G[yj][nbr].get(weight, 1)

        # Normalize the vector. The normalization denominator `norm`
        # should never be zero by the Perron--Frobenius
        # theorem. However, in case it is due to numerical error, we
        # assume the norm to be one instead.
        norm_x = sqrt(sum(z ** 2 for z in x.values())) or 1
        norm_y = sqrt(sum(z ** 2 for z in y.values())) or 1
        x = {k: v / norm_x for k, v in x.items()}
        y = {k: v / norm_y for k, v in y.items()}

        # Check for convergence (in the L_1 norm).
        if sum(abs(x[n] - xlast[n]) for n in x) < nnodes * tol:
            return(x,y)
    raise nx.PowerIterationFailedConvergence(max_iter)

