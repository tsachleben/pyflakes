#!/usr/bin/env python3
"""
snowflake.py: Draws a snowflake to out.png
"""

from argparse import ArgumentParser
from math import cos, pi, sin
from pathlib import Path

from pyx import canvas, path


def check_dir(dname):
  """ check_dir:
  """
  dpath = Path(dname)
  if not dpath.is_dir():
    raise ValueError
  return dpath

def num_range(bound_lt, bound_gt=None, v_type=int):
  """ num_range:
  """
  def _inner(val):
    val = v_type(val)
    if val < bound_lt:
      raise ValueError
    if bound_gt is not None and val > bound_gt:
      raise ValueError
    return val
  return _inner

def rad(theta):
  """ rad: convert degrees to radians
  """
  return pi * theta / 180

def carte(theta, radius=1):
  """ carte: convert polar to cartesian coordinates
  """
  return (radius*sin(theta), radius*cos(theta))

def vsum(a, b):
  """ vsum: Vector Sum of a and b
  """
  return (a[0] + b[0], a[1] + b[1])

def parse_args():
  """ parse_args: Parse Command Line Arguments
  """
  parser = ArgumentParser()
  parser.add_argument("--n_arms", metavar="N",
                      type=num_range(1), default=6)
  parser.add_argument("--len_k", metavar="K",
                      type=num_range(1), default=3)
  parser.add_argument("--len_b", metavar="B",
                      type=num_range(0, 1, v_type=float), default=.6667)
  parser.add_argument("--theta_i", metavar="T",
                      type=num_range(0, 90), default=40)
  parser.add_argument("--out_dir", metavar="dir",
                      type=check_dir, default=Path("."))
  return parser.parse_args()

def branch(sflake, len_e, theta_e, len_i, theta_i):
  """ branch:
  """
  root = carte(rad(theta_e), radius=len_e)
  tip_l = vsum(root, carte(rad(theta_e + theta_i), radius=len_i))
  tip_r = vsum(root, carte(rad(theta_e - theta_i), radius=len_i))
  sflake.stroke(path.path(path.moveto(*root), path.lineto(*tip_l)))
  sflake.stroke(path.path(path.moveto(*root), path.lineto(*tip_r)))

def main(n_arms, len_k, len_b, theta_i, out_dir):
  """ main: The core interpreter
  """
  sflake = canvas.canvas()
  for theta in range(0, 360, 360 // n_arms):
    coorid = carte(rad(theta), radius=len_k)
    sflake.stroke(path.path(path.moveto(0, 0), path.lineto(*coorid)))
    for len_e in range(1, len_k, 1):
      branch(sflake, len_e, theta, len_b, theta_i)
  sflake.writeGSfile(f"{out_dir}/snowflake-{n_arms}-{len_k}-{len_b}-{theta_i}.png")

if __name__ == '__main__':
  main(**vars(parse_args()))
