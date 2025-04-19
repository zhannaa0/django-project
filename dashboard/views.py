# dashboard/views.py

from django.shortcuts import render
from .forms import CSVUploadForm
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import uuid
from django.contrib.auth.decorators import login_required

@login_required
def upload_csv(request):
    context = {}
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_csv(file)

            context["columns"] = df.columns
            context["data"] = df.head(10).to_html(classes='table table-bordered')

            # Histogram for Performance Rating
            if 'Performance Rating' in df.columns:
                fig = px.histogram(df, x='Performance Rating', nbins=10, title='Performance Rating Distribution')
                context["chart"] = pio.to_html(fig, full_html=False)


            # Gauge chart for average productivity
            if 'Productivity Score' in df.columns:
                avg_productivity = df['Productivity Score'].mean()
                fig3 = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=avg_productivity,
                    number={'valueformat': '.2%'},
                    title={'text': "Average Productivity"},
                    gauge={
                        'axis': {'range': [0, 1], 'tickformat': ',.0%'},
                        'bar': {'color': "royalblue"},
                        'steps': [
                            {'range': [0, 0.6], 'color': "lightcoral"},
                            {'range': [0.6, 0.75], 'color': "gold"},
                            {'range': [0.75, 1.0], 'color': "lightgreen"},
                        ],
                    }
                ))
                context["chart3"] = pio.to_html(fig3, full_html=False)
    else:
        form = CSVUploadForm()

    context["form"] = form
    return render(request, "dashboard/upload.html", context)