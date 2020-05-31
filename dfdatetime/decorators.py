# -*- coding: utf-8 -*-
"""Function decorators."""

from __future__ import unicode_literals

import warnings
import typing

from typing import Any, Callable  # pylint: disable=unused-import


# pylint: disable=invalid-name
RETURN_TYPE = typing.TypeVar('RETURN_TYPE')


def deprecated(
    function: 'Callable[..., RETURN_TYPE]') -> 'Callable[..., RETURN_TYPE]':
  """Decorator to mark functions or methods as deprecated."""

  def IssueDeprecationWarning(*args: 'Any', **kwargs: 'Any') -> 'RETURN_TYPE':
    """Issue a deprecation warning."""
    warnings.simplefilter('default', DeprecationWarning)
    warnings.warn('Call to deprecated function: {0:s}.'.format(
        function.__name__), category=DeprecationWarning, stacklevel=2)

    return function(*args, **kwargs)

  IssueDeprecationWarning.__name__ = function.__name__
  IssueDeprecationWarning.__doc__ = function.__doc__
  IssueDeprecationWarning.__dict__.update(function.__dict__)
  return IssueDeprecationWarning
