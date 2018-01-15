"""
Created on July 10, 2017

@author: Jessica Ngo (jngo@bccrc.ca)
"""

#===========================
# Django imports
#---------------------------
from django.forms import (
    ModelForm,
    inlineformset_factory,
    modelform_factory,
    widgets,
    ModelChoiceField,
    ValidationError,
    Form
)

#===========================
# App imports
#---------------------------
from .models import *

from core.models import(
    DlpLibrary, DlpSequencing
)

#===========================
# Analysis forms (User)
#---------------------------
class AnalysisInformationForm(ModelForm):
    class Meta:
        model = AnalysisInformation
        fields = [
            'sequencings',
            'priority_level',
            'analysis_jira_ticket',
            'version',
        ]
        labels = {
            'sequencings':'Sequence(s)',
            'priority_level':'Priority Level',
            'analysis_jira_ticket':'Jira Ticket',
            'version':'Workflow',
        }
        help_texts = {
            'sequencings': 'Sequence(s) to analyze',
            'priority_level': 'Priority should match the urgency of this request.',
            'analysis_jira_ticket': 'Jira Ticket associated with this request',
            'version': 'Workflow and version to run',
        }
    def __init__(self, *args, **kwargs):
        library = kwargs.pop('library')
        super(AnalysisInformationForm, self).__init__(*args, **kwargs)
        self.fields['sequencings'].widget = widgets.CheckboxSelectMultiple()
        self.fields['sequencings'].queryset = DlpSequencing.objects.filter(library__pk = library.pk)


class AnalysisLibrarySelection(Form):
    library = ModelChoiceField(queryset=DlpLibrary.objects.all())

class ReferenceGenomeSelection(Form):
    ref_genome = ModelChoiceField(queryset=ReferenceGenome.objects.all())

#TODO add Reference genome dropdown, Sequencings, Add nice way to input JSON