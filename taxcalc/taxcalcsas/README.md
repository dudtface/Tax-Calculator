# Comparison of Tax-Calculator and TAXCALC SAS results

This directory includes tools used to compare the income tax results
generated by Tax-Calculator with results generated by the [TAXCALC SAS
program](http://www.nber.org/taxcalc) developed by Dan Feenberg and
Ina Shapiro of NBER with assistance from IRS-SOI staff.

The tools included in this directory are intended for use by the
Tax-Calculator core development team and support the following
cross-model-comparison work flow:

  1. Generate a sample of tax filing units (INPUT).
  2. Generate OUTPUT from INPUT using the inctax.py script.
  3. Generate OUTPUT from INPUT using the TAXCALC SAS program.
  4. Generate tax differences by comparing the two OUTPUT files.

Steps 1 and 2 are accomplished by the commands in the
[compare1](https://github.com/open-source-economics/Tax-Calculator/blob/master/taxcalc/taxcalcsas/compare1)
bash script (which will not execute on Windows).  Step 3 is
accomplished by (a) copying the INPUT file (as `compare-in.csv`), the
TAXCALC SAS program (`taxcalc.sas`), and the [compare.sas
script](https://github.com/open-source-economics/Tax-Calculator/blob/master/taxcalc/taxcalcsas/compare.sas)
to the same directory; (b) executing the `compare.sas` script; and (c)
copying back the resulting `compare-out.csv` file to the current
directory.  Step 4 is accomplished by the commands in the
[compare2](https://github.com/open-source-economics/Tax-Calculator/blob/master/taxcalc/taxcalcsas/compare2)
bash script (which will not execute on Windows).

## First comparisons

The initial phase of this comparison project involves generating three
separate INPUT files, each one of which contains 100,000 different
randomly-generated tax filing units for 2013.  The **a13** sample
units have no itemized deduction expenses and no childcare expenses.
The **b13** sample does have itemized deductions expenses, but no
childcare expenses.  And the **c13** sample has both itemized
deduction expenses and childcare expenses.

The samples are generated using these commands:

```
./compare1 a 13 ; ./compare1 b 13 ; ./compare1 c 13
```

The generated `a13.csv`, `b13.csv`, and `c13.csv` files are copied
(along with `compare.sas` and `taxcalc.sas`) to a directory where
`compare.sas` is executed by SAS.  The resulting `compare-out.csv`
files are copied back to this directory as `a13.out-sas`,
`b13.out-sas`, and `c13.out-sas`, respectively.  And finally, those
files are processed using these commands:

```
./compare2 a 13 ; ./compare2 b 13 ; ./compare2 c 13
```

The summary results of this comparison exercise are in three files:
[a13.taxdifferences](https://github.com/open-source-economics/Tax-Calculator/blob/master/taxcalc/taxcalcsas/a13-13.taxdifferences),
[b13.taxdifferences](https://github.com/open-source-economics/Tax-Calculator/blob/master/taxcalc/taxcalcsas/b13-13.taxdifferences), and
[c13.taxdifferences](https://github.com/open-source-economics/Tax-Calculator/blob/master/taxcalc/taxcalcsas/c13-13.taxdifferences).

The contents of these three cross-model-differences files are shown
here along with some commentary.

### a13 differences:

```
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 19     52     52      0.01 [874]
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 25     36     36      0.01 [2633]
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 27     71     71      0.01 [2665]
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 28     49     49      0.01 [874]
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]=  4     54     54     -0.01 [17158]
```

These a13 comparison results show that there are no differences
between `taxcalc.sas` and Tax-Calculator federal income tax
liabilities, or in several intermediate tax amounts, greater than one
cent.  However, these results ignore the fact that the current version
of Tax-Calculator does not calculate the Schedule R tax credit;
instead it reads it in from a more comprehensive input file than
`a13.csv`.  The `b13` and `c13` differences shown below also ignore
the Schedule R tax credit differences.

### b13 differences:

```
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 17   2086      0 -45500.00 [57063]
      #big_vardiffs_with_big_inctax_diff=              205
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 18   1306      0  29432.00 [81587]
      #big_vardiffs_with_big_inctax_diff=              205
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 19   1372     66   9712.56 [81587]
      #big_vardiffs_with_big_inctax_diff=              205
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 25     33     33      0.01 [1274]
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 27    507    196  -9712.56 [81587]
      #big_vardiffs_with_big_inctax_diff=              211
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 28    382     77   9712.56 [81587]
      #big_vardiffs_with_big_inctax_diff=              205
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]=  4    266     55  -3287.50 [75773]
                       #big_inctax_diffs=              211
```

These b13 comparison results show that there are very few (211 out of
100,000) units with income tax liabilities different by more than one
cent.  The largest income tax difference is almost $3300 (for the unit
with RECID 75773) with the Tax-Calculator amount being less that the
`taxcalc.sas` amount.  The causes of these few differences are being
investigated.

### c13 differences:

```
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 17   2123      0 -45350.00 [14914]
      #big_vardiffs_with_big_inctax_diff=              243
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 18   1333      0  31050.00 [39230]
      #big_vardiffs_with_big_inctax_diff=              243
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 19   1391     58   9696.72 [21201]
      #big_vardiffs_with_big_inctax_diff=              243
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 25     51     51      0.01 [1256]
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 27    537    202  -9696.72 [21201]
      #big_vardiffs_with_big_inctax_diff=              251
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]= 28    397     70   9696.72 [21201]
      #big_vardiffs_with_big_inctax_diff=              243
TAXDIFF:ovar,#diffs,#1cdiffs,maxdiff[id]=  4    328     77  -3150.00 [29984]
                       #big_inctax_diffs=              251
```

These c13 comparison results show that there are very few (251 out of
100,000) units with income tax liabilities different by more than one
cent.  The largest income tax difference is $3150 (for the unit
with RECID 29984) with the Tax-Calculator amount being less that the
`taxcalc.sas` amount.  The causes of these few differences are being
investigated.

## Subsequent comparisons

...