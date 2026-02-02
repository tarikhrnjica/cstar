# C* Language

This recreational and highly experimental project aims to construct a domain-agnostic, logic-centric programming language for quantum computers. Built as a Python embedded DSL, it explores how standard circuit manipulation can be replaced by the **Grothendieck-Isham topos** framework.

## Background

The name C* (pronounced "C-Star") is both, a pun relating it to the family of C languages, as well as an explicit nod to the C*-algebras that power it mathematically.

## Introduction

As quantum computers scale, it becomes convenient to transition from an imperative ("do this") approach to a more declarative ("make this true") paradigm. Rather than scheduling quantum gates manually (similar to Assembly), we wish to rely on a compiler to "glue" together our desired truths into a valid (globally consistent) quantum circuit. This shift in perspective turns an instruction like "Apply Hadamard to the given qubit" into the request "Ensure my system is entangled in a Bell state".
