// This is a part of rust-encoding.
//
// Any copyright is dedicated to the Public Domain.
// https://creativecommons.org/publicdomain/zero/1.0/

//! Japanese index tables for [rust-encoding](https://github.com/lifthrasiir/rust-encoding).

#![feature(phase)]

#[cfg(test)]
#[phase(plugin)]
extern crate encoding_index_tests;

/// JIS X 0208 with common extensions.
///
/// From the Encoding Standard:
///
/// > This is the JIS X 0208 standard including formerly proprietary extensions from IBM and NEC.
#[stable] pub mod jis0208;

/// JIS X 0212.
///
/// From the Encoding Standard:
///
/// > This is the JIS X 0212 standard.
/// > It is only used by the euc-jp decoder due to lack of widespread support elsewhere.
#[stable] pub mod jis0212;

