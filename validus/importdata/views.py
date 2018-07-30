from tablib import Dataset
# import numpy as np
import pandas as pd
import datetime

from django.shortcuts import render
from django.views.generic import TemplateView, CreateView

from .models import TimeSeries
from .resources import TimeSeriesResource
# from .forms import TimeSeriesForm


class ShowAllSheets(TemplateView):
    template_name = 'importdata/all.html'

    def get_context_data(self, **kwargs):
        ctx = super(ShowAllSheets, self).get_context_data(**kwargs)
        time_series_resource = TimeSeriesResource()
        queryset = TimeSeries.objects.all()
        dataset = time_series_resource.export(queryset)
        dataframe = dataset.df
        dataframe['valuation_date'] = pd.to_datetime(
            dataframe['valuation_date'], format='%d/%m/%Y')
        # print(dataframe['valuation_date'])
        # assert False
        year_one = dataframe.valuation_date[0].year
        num_days_in_year_one = dataframe[
            dataframe.valuation_date < datetime.datetime(
                year_one + 1, 1, 1)].shape[0]
        num_days_in_year_two = dataframe[
            dataframe.valuation_date < datetime.datetime(
                year_one + 2, 1, 1)].shape[0]
        num_days_in_year_three = dataframe[
            dataframe.valuation_date < datetime.datetime(
                year_one + 3, 1, 1)].shape[0]
        # dataframe.rolling(window=num_days_in_year_one).mean()
        # data_mean_year_one = pd.rolling(
        #     dataframe['mid'], window=num_days_in_year_one).mean()
        data_mean_year_one = dataframe['mid'].rolling(
            num_days_in_year_one).mean()
        data_mean_year_two = dataframe['mid'].rolling(
            num_days_in_year_two).mean()
        data_mean_year_three = dataframe['mid'].rolling(
            num_days_in_year_three).mean()
        data_std_year_one = dataframe['mid'].rolling(
            num_days_in_year_one).std()
        data_std_year_two = dataframe['mid'].rolling(
            num_days_in_year_two).std()
        data_std_year_three = dataframe['mid'].rolling(
            num_days_in_year_three).std()
        data_cov_year_one = dataframe['mid'].rolling(
            num_days_in_year_one).cov()
        data_cov_year_two = dataframe['mid'].rolling(
            num_days_in_year_two).cov()
        data_cov_year_three = dataframe['mid'].rolling(
            num_days_in_year_three).cov()
        data_corr_year_one = dataframe['mid'].rolling(
            num_days_in_year_one).corr()
        data_corr_year_two = dataframe['mid'].rolling(
            num_days_in_year_two).corr()
        data_corr_year_three = dataframe['mid'].rolling(
            num_days_in_year_three).corr()
        # print(data_mean_year_one)
        # assert False
        append_col = [0] + [round((dataset['mid'][i + 1] / dataset['mid'][i]) - 1, 4)
                            for i in range(queryset.count() - 1)]
        dataset.append_col(append_col, header="Returns")
        dataset.append_col(data_mean_year_one, header='1 Yr Mean')
        dataset.append_col(data_mean_year_two, header='2 Yr Mean')
        dataset.append_col(data_mean_year_three, header='3 Yr Mean')
        dataset.append_col(data_std_year_one, header='1 Yr Std')
        dataset.append_col(data_std_year_two, header='2 Yr Std')
        dataset.append_col(data_std_year_three, header='3 Yr Std')
        dataset.append_col(data_cov_year_one, header='1 Yr Cov')
        dataset.append_col(data_cov_year_two, header='2 Yr Cov')
        dataset.append_col(data_cov_year_three, header='3 Yr Cov')
        dataset.append_col(data_corr_year_one, header='1 Yr Corr')
        dataset.append_col(data_corr_year_two, header='2 Yr Corr')
        dataset.append_col(data_corr_year_three, header='3 Yr Corr')
        ctx['sheets'] = dataset.html
        return ctx


class AddNewSheet(CreateView):
    template_name = 'importdata/add_new.html'
    model = TimeSeries
    fields = ['sheet_name']


def upload_sheet(request):
    if request.method == 'POST':
        time_series_resource = TimeSeriesResource()
        dataset = Dataset()
        new_time_series = request.FILES['myfile']
        imported_data = dataset.load(
            new_time_series.read().decode('utf-8'),
            format='csv', delimiter=';')
        result = time_series_resource.import_data(imported_data, dry_run=True)
        # Test the data import

        if not result.has_errors():
            time_series_resource.import_data(imported_data, dry_run=False)
            # Actually import now
            table = imported_data.html
            return render(
                request, 'importdata/upload_sheet.html', {'table': table})
    return render(request, 'importdata/upload_sheet.html')
