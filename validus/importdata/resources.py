from import_export import resources, fields, widgets
from .models import TimeSeries


class TimeSeriesResource(resources.ModelResource):
    valuation_date = fields.Field(
        column_name='valuation_date', attribute='valuation_date',
        widget=widgets.DateWidget(format='%d/%m/%Y'))

    def before_import(self, dataset, *args, **kwargs):
        if 'id' not in dataset.headers:
            dataset.insert_col(0, lambda row: "", header='id')
        if dataset.headers:
            dataset.headers = [str(header).lower().strip()
                               for header in dataset.headers]

    class Meta:
        model = TimeSeries
        # skip_unchanged = True
        # report_skipped = True
        fields = ['id', 'valuation_date', 'underlying', 'mid']
        import_id_fields = ['id', ]
