from cgitb import html
from operator import sub
from unicodedata import category
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, JsonResponse
import plotly
from .models import Budget,Actuals,Category
from .forms import budget_form, categories_form, actuals_form,date_form,year_form
from datetime import date, datetime
from django.db.models import Sum
import pytz
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.express as px
import plotly.offline as opy
from plotly.subplots import make_subplots
from django.core import serializers
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# Create your views here.


def dashboard(request):

    return render(request,'budget/dashboard.html',{'Hello':'Hello'})

@login_required(login_url= 'login')
def add_budget(request):

    b_form = budget_form(user=request.user)
    if request.method == 'POST' and "budgetForminfo" in request.POST:
        
        b_form = budget_form(request.POST or None)
        
        if b_form.is_valid():
            
            b_form = budget_form(request.POST or None,request.FILES,user = request.user)
            b_form.save()
            b_form = budget_form()
            return redirect('add_budget')

    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    
    m_text = ""
    y_text = ""

    
    d_form = date_form
    if request.method == 'POST' and "get_month" in request.POST:
        d_form = date_form(request.POST or None)
        if d_form.is_valid():
            m_text = d_form.cleaned_data['months']
            y_text = d_form.cleaned_data['years']

    
    if not m_text:
       monthForsearch = '{:02d}'.format(currentMonth)
       yearForsearch = str(currentYear)
    else:
        monthForsearch = m_text
        yearForsearch = y_text

    
    income = Budget.objects.filter(category__user = request.user,category__income_or_expense = 'Income',date__year = yearForsearch, date__month = monthForsearch)
    expense = Budget.objects.filter(category__user = request.user,category__income_or_expense = 'Expense',date__year = yearForsearch, date__month = monthForsearch)

    tot_inc = Budget.objects.filter(category__user = request.user,category__income_or_expense = 'Income',date__year = yearForsearch, date__month = monthForsearch).aggregate(Sum('budget_amt'))
    tot_exp = Budget.objects.filter(category__user = request.user,category__income_or_expense = 'Expense',date__year = yearForsearch, date__month = monthForsearch).aggregate(Sum('budget_amt'))

    templateMonth = str(int(monthForsearch))
    datetime_object = datetime.strptime(templateMonth, "%m")
    month_name = datetime_object.strftime("%B")




    if len(income) == 0 or len(expense) == 0 :

        error  = 'Please Budget Income & Expense to see data'

        return render(request,'budget/add_budget.html',{'b_form':b_form,'error':error,'d_form':d_form,'yearForsearch':yearForsearch,'month_name':month_name,'expense':expense,'income':income})

    


    saved = tot_inc['budget_amt__sum'] - tot_exp['budget_amt__sum']

    tot_saved = "{:,.2f}".format(saved)
    tot_inc_float = "{:,.2f}".format(tot_inc['budget_amt__sum'])
    tot_exp_float = "{:,.2f}".format(tot_exp['budget_amt__sum'])


    

    

    


    return render(request,'budget/add_budget.html',{'b_form':b_form,'d_form':d_form,'expense':expense,'income':income,'monthForsearch':monthForsearch, 'month_name':month_name, 'yearForsearch':yearForsearch,'tot_inc': tot_inc_float,'tot_exp':tot_exp_float,'tot_saved':tot_saved})

@login_required(login_url= 'login')
def edit_budget(request,pk):

    budLine = Budget.objects.get(id=pk)
    editBudgetform = budget_form(instance = budLine,user=request.user )
    if request.method == 'POST' and "editBudgetform" in request.POST:
        editBudgetform = budget_form(request.POST or None,instance = budLine)
        if editBudgetform.is_valid():
                editBudgetform = budget_form(request.POST or None,request.FILES, user=request.user,instance = budLine)
                editBudgetform.save()
                editBudgetform = budget_form()
                return redirect('add_budget')
        
    return render(request,'budget/edit_budget.html',{'editBudgetform':editBudgetform})

@login_required(login_url= 'login')
def delete_budget(request,pk):
    budDel = Budget.objects.get(id=pk)
    budDel.delete()
    return redirect('add_budget')

@login_required(login_url= 'login')
def add_actuals(request):

    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    text = ""
    y_text = ""

    
    d_form = date_form
    if request.method == 'POST' and "get_month" in request.POST:
        d_form = date_form(request.POST or None)
        if d_form.is_valid():
            text = d_form.cleaned_data['months']
            y_text = d_form.cleaned_data['years']

    
    if not text:
       monthForsearch = '{:02d}'.format(currentMonth)
       yearForsearch = str(currentYear)
    else:
        monthForsearch = text
        yearForsearch = y_text


    income_act = Actuals.objects.filter(category__user = request.user,category__income_or_expense = 'Income',date__year = yearForsearch, date__month = monthForsearch)
    expense_act = Actuals.objects.filter(category__user = request.user,category__income_or_expense = 'Expense',date__year = yearForsearch, date__month = monthForsearch)

    

    form = actuals_form(user=request.user)
    if request.method == 'POST' and "actuals_form" in request.POST:
        form = actuals_form(request.POST)
        if form.is_valid():
            form = actuals_form(request.POST or None,request.FILES, user=request.user)
            form.save()
            form = actuals_form()
            return redirect('add_actuals')


    templateMonth = str(int(monthForsearch))
    datetime_object = datetime.strptime(templateMonth, "%m")
    month_name = datetime_object.strftime("%B")

    return render(request,'budget/add_actuals.html',{'d_form':d_form,'form':form,'income_act':income_act,'expense_act':expense_act, 'month_name':month_name, 'yearForsearch':yearForsearch})

@login_required(login_url= 'login')
def edit_actuals(request,pk):

    
    actLine = Actuals.objects.get(id=pk)
    editActualsform = actuals_form(instance = actLine,user=request.user)

    if request.method == 'POST' and "editActualsform" in request.POST:
        editActualsform = actuals_form(request.POST or None,instance = actLine)
        if editActualsform.is_valid():
            editActualsform = actuals_form(request.POST or None,request.FILES, user=request.user,instance = actLine)
            editActualsform.save()
            editActualsform = actuals_form()
            return redirect('add_actuals')

    
    return render(request,'budget/edit_actuals.html',{'editActualsform':editActualsform})


@login_required(login_url= 'login')
def delete_actuals(request,pk):
    actDel = Actuals.objects.get(id=pk)
    actDel.delete()
    return redirect('add_actuals')

@login_required(login_url= 'login')
def add_category(request):

    form = categories_form

    if request.method == 'POST':
        form = categories_form(request.POST)
        if form.is_valid():
            form.save(commit= False)
            form.instance.user = request.user
            form.save()
            return redirect('add_budget')

    

    return render(request,'budget/add_category.html',{'form':form})


@login_required(login_url= 'login')
def monthly(request):


    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    
    text = ""
    y_text = ""

    
    d_form = date_form
    if request.method == 'POST' and "get_month" in request.POST:
        d_form = date_form(request.POST or None)
        if d_form.is_valid():
            text = d_form.cleaned_data['months']
            y_text = d_form.cleaned_data['years']

    
    if not text:
       monthForsearch = '{:02d}'.format(currentMonth)
       yearForsearch = str(currentYear)

    else:
        monthForsearch = text
        yearForsearch = y_text



    act_exp = Actuals.objects.filter(category__user = request.user,category__income_or_expense = 'Expense', date__year = yearForsearch ,date__month = monthForsearch).values('category__category_feild','date').order_by('category__category_feild').annotate(total_actuals = Sum('transactions_amount'))
    act_inc = Actuals.objects.filter(category__user = request.user,category__income_or_expense = 'Income', date__year = yearForsearch ,date__month = monthForsearch).values('category__category_feild','date').order_by('category__category_feild').annotate(total_actuals = Sum('transactions_amount'))
        
    bud_exp =  Budget.objects.filter(category__user = request.user,category__income_or_expense = 'Expense',date__year = yearForsearch, date__month = monthForsearch).values('category__category_feild','date','comments').annotate(total_budget = Sum('budget_amt'))
    bud_inc = Budget.objects.filter(category__user = request.user,category__income_or_expense = 'Income',date__year = yearForsearch, date__month = monthForsearch).values('category__category_feild','date','comments').annotate(total_budget = Sum('budget_amt'))


    # to grab actual expanses

    act_exp_Category = []
    act_exp_Date = []
    act_exp_Actual = []


    for i in range(0,len(act_exp)):
        act_exp_Category.append(act_exp[i]['category__category_feild'])
        act_exp_Date.append(act_exp[i]['date'])
        act_exp_Actual.append(act_exp[i]['total_actuals'])

        
        
    act_exp_df = pd.DataFrame({'Category' : act_exp_Category, 'Actual': act_exp_Actual,'Date': act_exp_Date })

    act_exp_final = pd.DataFrame(act_exp_df.groupby('Category')['Actual'].sum())



        # to grab actual income

    act_inc_Category = []
    act_inc_Date = []
    act_inc_Actual = []


    for i in range(0,len(act_inc)):
        act_inc_Category.append(act_inc[i]['category__category_feild'])
        act_inc_Date.append(act_inc[i]['date'])
        act_inc_Actual.append(act_inc[i]['total_actuals'])

    act_inc_df = pd.DataFrame({'Category' : act_inc_Category, 'Actual': act_inc_Actual,'Date': act_inc_Date })

    act_inc_final = pd.DataFrame(act_inc_df.groupby('Category')['Actual'].sum())


        # grab budgeted expenses 

    bud_exp_Category = []
    bud_exp_Date = []
    bud_exp_Actual = []


    for i in range(0,len(bud_exp)):
        bud_exp_Category.append(bud_exp[i]['category__category_feild'])
        bud_exp_Date.append(bud_exp[i]['date'])
        bud_exp_Actual.append(bud_exp[i]['total_budget'])

    bud_exp_df = pd.DataFrame({'Category' : bud_exp_Category, 'Budget': bud_exp_Actual,'Date': bud_exp_Date })

    bud_exp_final = pd.DataFrame(bud_exp_df.groupby('Category')['Budget'].sum())

    # grab budgeted income

    bud_inc_Category = []
    bud_inc_Date = []
    bud_inc_Actual = []


    for i in range(0,len(bud_inc)):
        bud_inc_Category.append(bud_inc[i]['category__category_feild'])
        bud_inc_Date.append(bud_inc[i]['date'])
        bud_inc_Actual.append(bud_inc[i]['total_budget'])

    bud_inc_df = pd.DataFrame({'Category' : bud_inc_Category, 'Budget': bud_inc_Actual,'Date': bud_inc_Date })

    bud_inc_final = pd.DataFrame(bud_inc_df.groupby('Category')['Budget'].sum())



        # to merge budget and actuals expenses

    exp_result = pd.merge(act_exp_final,bud_exp_final,how = 'outer' ,on = 'Category').fillna(0)
    exp_result['Variance'] =  exp_result.Budget - exp_result.Actual
    exp_result.round(1)
    exp_result.reset_index(inplace = True)
    exp_json_records = exp_result.reset_index().to_json(orient ='records')

    exp_data = []

    exp_data = json.loads(exp_json_records)

    # to merge budget and actuals income

    inc_result = pd.merge(act_inc_final,bud_inc_final, how = 'outer',on = 'Category').fillna(0)
    inc_result['Variance'] =  inc_result.Actual - inc_result.Budget
    inc_result.round(1)
    inc_result.reset_index(inplace = True)
    inc_json_records = inc_result.reset_index().to_json(orient ='records')
    inc_data = []
    inc_data = json.loads(inc_json_records)


    oig = go.Figure()

    oig.add_trace(go.Histogram(histfunc="sum", y= exp_result['Budget'], x=exp_result['Category'], name="Budget"))
    oig.add_trace(go.Histogram(histfunc="sum", y=exp_result['Actual'], x=exp_result['Category'], name="Actual"))
    oig.update_layout(
                    title_text="Actual V Budget",plot_bgcolor='rgba(0,0,0,0)')

    histo_chart = oig.to_html(full_html=False,default_height=600, default_width=1300, include_plotlyjs='cdn')


    pig = go.Figure(data=[go.Pie(labels= exp_result['Category'], values= exp_result['Actual'], name = "Actual Expense")])
    pig.update_layout(
                    title_text="Spend Insight")
    pie_chart = pig.to_html(full_html=False,default_height=600, default_width=1300)


    templateMonth = str(int(monthForsearch))
    datetime_object = datetime.strptime(templateMonth, "%m")
    month_name = datetime_object.strftime("%B")


    total_expense = exp_result['Actual'].sum()
    total_income = inc_result['Actual'].sum()
    saved = total_income - total_expense

    
    total_expense_float = "{:,.2f}".format(total_expense)
    total_income_float = "{:,.2f}".format(total_income)
    saved_float = "{:,.2f}".format(saved)


    if len(bud_exp) == 0:

        error  = 'No Data For Selected Date - Start Budgeting !'

        return render(request,'budget/monthly.html',{'error':error,'d_form':d_form,'yearForsearch':yearForsearch, 'monthForsearch':monthForsearch,'month_name':month_name})

    

       

    return render(request,'budget/monthly.html',{'d_form':d_form,'inc_data':inc_data,'exp_data':exp_data,'histo_chart':histo_chart,'pie_chart':pie_chart, 'month_name':month_name,'yearForsearch':yearForsearch, 'total_income':total_income_float,'total_expense':total_expense_float,'saved':saved_float})

@login_required(login_url= 'login')
def yearly(request):


    #currentMonth = datetime.now().month
    currentYear = datetime.now().year
    
    #text = ""
    y_text = ""

    
    d_form = year_form
    if request.method == 'POST' and "get_year" in request.POST:
        d_form = year_form(request.POST or None)
        if d_form.is_valid():
            #text = d_form.cleaned_data['months']
            y_text = d_form.cleaned_data['years']

    
    if not y_text:
       #monthForsearch = '{:02d}'.format(currentMonth)
       yearForsearch = str(currentYear)

    else:
       # monthForsearch = text
        yearForsearch = y_text



    act_exp = Actuals.objects.filter(category__user = request.user,category__income_or_expense = 'Expense', date__year = yearForsearch).values('category__category_feild','date').order_by('category__category_feild').annotate(total_actuals = Sum('transactions_amount'))
    act_inc = Actuals.objects.filter(category__user = request.user,category__income_or_expense = 'Income', date__year = yearForsearch ).values('category__category_feild','date').order_by('category__category_feild').annotate(total_actuals = Sum('transactions_amount'))
        
    bud_exp =  Budget.objects.filter(category__user = request.user,category__income_or_expense = 'Expense',date__year = yearForsearch).values('category__category_feild','date','comments').annotate(total_budget = Sum('budget_amt'))
    bud_inc = Budget.objects.filter(category__user = request.user,category__income_or_expense = 'Income',date__year = yearForsearch).values('category__category_feild','date','comments').annotate(total_budget = Sum('budget_amt'))


    # to grab actual expenses

    act_exp_Category = []
    act_exp_Date = []
    act_exp_Actual = []


    for i in range(0,len(act_exp)):
        act_exp_Category.append(act_exp[i]['category__category_feild'])
        act_exp_Date.append(act_exp[i]['date'])
        act_exp_Actual.append(act_exp[i]['total_actuals'])

        
        
    act_exp_df = pd.DataFrame({'Category' : act_exp_Category, 'Actual': act_exp_Actual,'Date': act_exp_Date })

    act_exp_final = pd.DataFrame(act_exp_df.groupby('Category')['Actual'].sum())



        # to grab actual income

    act_inc_Category = []
    act_inc_Date = []
    act_inc_Actual = []


    for i in range(0,len(act_inc)):
        act_inc_Category.append(act_inc[i]['category__category_feild'])
        act_inc_Date.append(act_inc[i]['date'])
        act_inc_Actual.append(act_inc[i]['total_actuals'])

    act_inc_df = pd.DataFrame({'Category' : act_inc_Category, 'Actual': act_inc_Actual,'Date': act_inc_Date })

    act_inc_final = pd.DataFrame(act_inc_df.groupby('Category')['Actual'].sum())


        # grab budgeted expenses 

    bud_exp_Category = []
    bud_exp_Date = []
    bud_exp_Actual = []


    for i in range(0,len(bud_exp)):
        bud_exp_Category.append(bud_exp[i]['category__category_feild'])
        bud_exp_Date.append(bud_exp[i]['date'])
        bud_exp_Actual.append(bud_exp[i]['total_budget'])

    bud_exp_df = pd.DataFrame({'Category' : bud_exp_Category, 'Budget': bud_exp_Actual,'Date': bud_exp_Date })

    bud_exp_final = pd.DataFrame(bud_exp_df.groupby('Category')['Budget'].sum())

    # grab budgeted income

    bud_inc_Category = []
    bud_inc_Date = []
    bud_inc_Actual = []


    for i in range(0,len(bud_inc)):
        bud_inc_Category.append(bud_inc[i]['category__category_feild'])
        bud_inc_Date.append(bud_inc[i]['date'])
        bud_inc_Actual.append(bud_inc[i]['total_budget'])

    bud_inc_df = pd.DataFrame({'Category' : bud_inc_Category, 'Budget': bud_inc_Actual,'Date': bud_inc_Date })

    bud_inc_final = pd.DataFrame(bud_inc_df.groupby('Category')['Budget'].sum())



        # to merge budget and actuals expenses

    exp_result = pd.merge(act_exp_final,bud_exp_final,how = 'outer' ,on = 'Category').fillna(0)
    exp_result['Variance'] =  exp_result.Budget - exp_result.Actual
    exp_result.round(1)
    exp_result.reset_index(inplace = True)
    exp_json_records = exp_result.reset_index().to_json(orient ='records')

    exp_data = []

    exp_data = json.loads(exp_json_records)

    # to merge budget and actuals income

    inc_result = pd.merge(act_inc_final,bud_inc_final, how = 'outer',on = 'Category').fillna(0)
    inc_result['Variance'] =  inc_result.Actual - inc_result.Budget
    inc_result.round(1)
    inc_result.reset_index(inplace = True)
    inc_json_records = inc_result.reset_index().to_json(orient ='records')
    inc_data = []
    inc_data = json.loads(inc_json_records)


    


    oig = go.Figure()

    oig.add_trace(go.Histogram(histfunc="sum", y= exp_result['Budget'], x=exp_result['Category'], name="Budget"))
    oig.add_trace(go.Histogram(histfunc="sum", y=exp_result['Actual'], x=exp_result['Category'], name="Actual"))

    oig.update_layout(
                    title_text="Actual V Budget",plot_bgcolor='rgba(0,0,0,0)')

    histo_chart = oig.to_html(full_html=False,default_height=600, default_width=1300, include_plotlyjs='cdn')


    pig = go.Figure(data=[go.Pie(labels= exp_result['Category'], values= exp_result['Actual'], name = "Actual Expense")])
    pig.update_layout(
                    title_text="Spend Insight")
    pie_chart = pig.to_html(full_html=False,default_height=600, default_width=1300)


    if len(bud_exp) == 0 or len(act_exp)== 0 or len(act_inc)== 0 or len(act_exp)== 0  :

        error  = 'Graph will show once Budget & Actuals are populated!'

        return render(request,'budget/yearly.html',{'error':error,'d_form':d_form,'yearForsearch':yearForsearch,'inc_data':inc_data,'exp_data':exp_data})


    #to group actual expenses by date 
    df_actual_expense = pd.DataFrame(list(zip(act_exp_Category,act_exp_Date,act_exp_Actual)), columns=['Category', 'Date', 'Actual'])
    dg = df_actual_expense .groupby(pd.Grouper(key='Date', freq='1M')).sum()
    df_3 = dg.reset_index()
    df_3['Date'] = df_3['Date'].apply(pd.to_datetime)

    #to group budgeted expenses by date
    df_budget_expense = pd.DataFrame(list(zip(bud_exp_Category,bud_exp_Date,bud_exp_Actual)), columns=['Category', 'Date', 'Budget'])
    dg_1 = df_budget_expense .groupby(pd.Grouper(key='Date', freq='1M')).sum()
    df_2 = dg_1.reset_index()
    df_2['Date'] = df_2['Date'].apply(pd.to_datetime)

    #to group Actual Income by date
    df_actual_income = pd.DataFrame(list(zip(act_inc_Category,act_inc_Date,act_inc_Actual)), columns=['Category', 'Date', 'Actual'])
    dg_2 = df_actual_income .groupby(pd.Grouper(key='Date', freq='1M')).sum()
    df_1 = dg_2.reset_index()
    df_1['Date'] = df_1['Date'].apply(pd.to_datetime)


    



    fig = go.Figure()

    fig.add_trace(go.Scatter(name="Actual Expenses",
    x=df_3["Date"], y=df_3["Actual"],xperiod="M1"))

    fig.add_trace(go.Scatter(name="Budget Expenses",
    x=df_2["Date"], y=df_2["Budget"],xperiod="M1"))

    fig.add_trace(go.Scatter(name="Actual Income",
    x=df_1["Date"], y=df_1["Actual"],xperiod="M1"))


                                                                                     
                                                    
    fig.update_xaxes(showgrid=False)
    #fig.update_layout(xaxis=dict(tickformat='%B %Y'))
    fig.update_layout(xaxis_range=['{}-01-01'.format(yearForsearch),'{}-12-31'.format(yearForsearch)],
                    title_text="Trend Insight",plot_bgcolor='rgba(0,0,0,0)')
    trend_fig = fig.to_html(full_html=False,default_height=500, default_width=1400)


        


    #templateMonth = str(int(monthForsearch))
    #datetime_object = datetime.strptime(templateMonth, "%m")
    #month_name = datetime_object.strftime("%B")


    total_expense = exp_result['Actual'].sum()
    total_income = inc_result['Actual'].sum()
    saved = total_income - total_expense

    
    total_expense_float = "{:,.2f}".format(total_expense)
    total_income_float = "{:,.2f}".format(total_income)
    saved_float = "{:,.2f}".format(saved)


    

    

       

    return render(request,'budget/yearly.html',{'d_form':d_form,'inc_data':inc_data,'exp_data':exp_data,'histo_chart':histo_chart,'pie_chart':pie_chart,'yearForsearch':yearForsearch, 'total_income':total_income_float,'total_expense':total_expense_float,'saved':saved_float,'trend_fig':trend_fig})

@login_required(login_url= 'login')
def category_manager(request):

    cats = Category.objects.filter(user = request.user)


    return render(request, 'budget/category_manager.html',{'cats':cats} )


@login_required(login_url= 'login')
def edit_category(request,pk):

    catLine = Category.objects.get(id=pk)
    editCatform = categories_form(instance = catLine)

    if request.method == 'POST' and "editCatform" in request.POST:
        editCatform = categories_form(request.POST or None,instance = catLine)
        if editCatform.is_valid():
                editCatform.save()
                editCatform=categories_form()
                return redirect('category_manager')


    return render(request, 'budget/edit_category.html',{'editCatform':editCatform} )


