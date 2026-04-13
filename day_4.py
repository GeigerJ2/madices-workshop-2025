#!/usr/bin/env python
# coding: utf-8

# # AiiDA

# In[1]:


from aiida_workgraph import task, spec


# In[2]:


from aiida import load_profile
load_profile()


# In[3]:


@task(outputs=['prod', 'div'])
def get_prod_and_div(x, y):
    return {"prod": x * y, "div": x / y}


# In[4]:


@task
def get_sum(x, y):
    return x + y


# In[5]:


@task
def get_square(x):
    return x ** 2


# In[6]:


@task.graph
def get_inner_part(a, b):
    prod_and_div = get_prod_and_div(x=a, y=b)
    return get_sum(x=prod_and_div.prod, y=prod_and_div.div).result


# In[7]:


@task.graph
def get_total_workflow(c, d):
    tmp_sum = get_inner_part(a=c, b=d).result
    return get_square(x=tmp_sum).result


# In[8]:


wg = get_total_workflow.build(c=1, d=2)
wg.run()


# # jobflow

# In[9]:


from jobflow import job, Flow, run_locally


# In[10]:


@job
def get_prod_and_div(x, y):
    return {"prod": x * y, "div": x / y}


# In[11]:


@job
def get_sum(x, y):
    return x + y


# In[12]:


@job
def get_square(x):
    return x ** 2


# In[13]:


prod_and_div = get_prod_and_div(x=1, y=2)
tmp_sum = get_sum(x=prod_and_div.output.prod, y=prod_and_div.output.div)
inner_flow = Flow([prod_and_div, tmp_sum], output=tmp_sum.output)
result = get_square(x=inner_flow.output)
total_workflow = Flow([inner_flow, result])


# In[14]:


run_locally(total_workflow)


# # pyiron_base

# In[15]:


from pyiron_base import job


# In[16]:


@job(output_key_lst=['prod', 'div'])
def get_prod_and_div(x, y):
    return {"prod": x * y, "div": x / y}


# In[17]:


@job
def get_sum(x, y):
    return x + y


# In[18]:


@job
def get_square(x):
    return x ** 2


# In[19]:


@job
def get_inner_part(a, b):
    prod_and_div = get_prod_and_div(x=1, y=2)
    return get_sum(x=prod_and_div.output.prod, y=prod_and_div.output.div).pull()


# In[20]:


@job
def get_total_workflow(c, d):
    tmp_sum = get_inner_part(a=c, b=d)
    return get_square(x=tmp_sum).pull()


# In[21]:


result = get_total_workflow(c=1, d=2)


# In[22]:


result.pull()

