# commerado-gadgets

Card templates for Commerado chat cards. Templates and product photos only: no sales data, no secrets.
Chat cards load a tagged file through jsDelivr and pass the numbers in.

| File | Card | Built by |
|---|---|---|
| sales-today.js | Sales by marketplace, tap to see SKUs with photo, amount and units | build/build_sales.py |

Use a version tag (for example `@v1`): jsDelivr serves a new tag at once, but caches a branch for up to 12 hours.

```html
<div id="cg"></div>
<script>window.CG_DATA = {title: 'Sales - Thu 12 Nov', subtitle: 'Amazon - full day', total: 17942, refunds: 714, net: 17228,
  mk: [{name: 'MeaMarket UAE', amount: 11959, units: 152, skus: [['PEGANT_PG550', 2493, 32]]}]};</script>
<script src="https://cdn.jsdelivr.net/gh/bravezlecoeur/commerado-gadgets@v1/sales-today.js"></script>
```
