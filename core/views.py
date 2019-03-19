"""
Created on May 16, 2016

@author: Jafar Taghiyar (jtaghiyar@bccrc.ca)

Updated by Spencer Vatrt-Watts (github.com/Spenca)
"""

import os
import collections
import subprocess
from jira import JIRA, JIRAError

#============================
# Django imports
#----------------------------
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required #, permission_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.generic.base import TemplateView, View
from django.db import transaction
from django.forms.models import model_to_dict

import pandas as pd
from django.conf import settings
from django.utils import timezone
from itertools import chain
import json


#============================
# App imports
#----------------------------
from .helpers import Render
from .models import (
    Sample,
    DlpLibrary,
    DlpSequencing,
    PbalLibrary,
    PbalSequencing,
    TenxLibrary,
    TenxCondition,
    TenxChip,
    TenxSequencing,
    DlpLane,
    PbalLane,
    TenxLane,
    SublibraryInformation,
    ChipRegion,
    ChipRegionMetadata,
    MetadataField,
    Plate,
    Library,
    JiraUser,
    Project)
from sisyphus.models import *
from .forms import (
    SampleForm,
    AdditionalSampleInfoInlineFormset,
    DlpLibraryForm,
    PbalLibraryForm,
    TenxLibraryForm,
    DlpLibrarySampleDetailInlineFormset,
    DlpLibraryConstructionInfoInlineFormset,
    DlpLibraryQuantificationAndStorageInlineFormset,
    PbalLibrarySampleDetailInlineFormset,
    PbalLibraryConstructionInfoInlineFormset,
    PbalLibraryQuantificationAndStorageInlineFormset,
    TenxLibrarySampleDetailInlineFormset,
    TenxLibraryConstructionInfoInlineFormset,
    TenxLibraryQuantificationAndStorageInlineFormset,
    SublibraryForm,
    DlpSequencingForm,
    PbalSequencingForm,
    TenxSequencingForm,
    DlpLaneForm,
    PbalLaneForm,
    TenxLaneForm,
    GSCFormDeliveryInfo,
    GSCFormSubmitterInfo,
    TenxConditionFormset,
    ProjectForm,
    PlateForm,
    JiraConfirmationForm,
    AddWatchersForm,
    TenxChipForm)
from .utils import (
    create_sublibrary_models,
    generate_samplesheet,
    generate_gsc_form,
)
from .jira_templates.templates import (
    get_reference_genome_from_sample_id,
    generate_dlp_jira_description,
    generate_tenx_jira_description,
)

from .jira_templates.jira_wrapper import (
    create_ticket,
    get_projects,
    get_project_id_from_name,
    validate_credentials,
    add_watchers,
    add_jira_comment,
    update_description,
)

from colossus.settings import LOGIN_URL



from colossus.settings import LOGIN_URL

#============================
# Index page
#----------------------------
class IndexView(LoginRequiredMixin, TemplateView):
    """
    Home page.
    """
    login_url = LOGIN_URL
    template_name = "core/index.html"

    def get_context_data(self):
        context = {
            'sample_size': Sample.objects.count(),
            'dlp_library_size': DlpLibrary.objects.count(),
            'dlp_sequencing_size': DlpSequencing.objects.count(),
            'pbal_library_size': PbalLibrary.objects.count(),
            'pbal_sequencing_size': PbalSequencing.objects.count(),
            'tenx_library_size': TenxLibrary.objects.count(),
            'tenx_sequencing_size': TenxSequencing.objects.count(),
            'tenx_chips_size': TenxChip.objects.count(),
            'analysisinformation_size':DlpAnalysisInformation.objects.count(),
            'analysisrun_size':AnalysisRun.objects.count(),
        }
        return context


#============================
# Sample views
#----------------------------
class SampleList(LoginRequiredMixin, TemplateView):
    """
    List of samples.
    """
    login_url = LOGIN_URL
    template_name = "core/sample_list.html"

    def get_context_data(self):
        context = {
            'samples': Sample.objects.all().order_by('sample_id'),
        }
        return context


class Inventory(SampleList):

    """
    Inventory of sequencings associated with samples.
    """

    template_name = "core/inventory.html"


class SampleDetail(LoginRequiredMixin, TemplateView):
    """
    Sample detail page.
    """
    login_url = LOGIN_URL
    template_name = "core/sample_detail.html"

    def get_context_data(self, pk):
        context = {
            'sample': get_object_or_404(Sample, pk=pk),
            'library_list': ['dlp', 'pbal', 'tenx'],
            'pk': pk,
        }
        return context


class SampleCreate(LoginRequiredMixin, TemplateView):
    """
    Sample create page.
    """
    login_url = LOGIN_URL
    template_name="core/sample_create.html"

    def get_context_and_render(self, request, form, formset, pk=None):
        context = {
            'pk': pk,
            'form': form,
            'formset': formset,
        }
        return render(request, self.template_name, context)

    def get(self, request):
        form = SampleForm()
        formset = AdditionalSampleInfoInlineFormset()
        return self.get_context_and_render(request, form, formset)

    def post(self, request):
        form = SampleForm(request.POST)
        formset = AdditionalSampleInfoInlineFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            formset.instance = instance
            instance.save()
            formset.save()
            msg = "Successfully created the Sample."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.get_absolute_url())

        msg = "Failed to create the sample. Please fix the errors below."
        messages.error(request, msg)
        return self.get_context_and_render(request, form, formset)


class SampleUpdate(SampleCreate):

    """
    Sample update page.
    """

    template_name = "core/sample_update.html"

    def get(self, request, pk):
        sample = get_object_or_404(Sample, pk=pk)
        form=SampleForm(instance=sample)
        formset=AdditionalSampleInfoInlineFormset(instance=sample)
        return self.get_context_and_render(request, form, formset, pk=pk)

    def post(self, request, pk):
        sample = get_object_or_404(Sample, pk=pk)
        form = SampleForm(request.POST, instance=sample)
        formset = AdditionalSampleInfoInlineFormset(request.POST, instance=sample)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            msg = "Successfully updated the Sample."
            messages.success(request, msg)
            return HttpResponseRedirect(sample.get_absolute_url())

        msg = "Failed to update the sample. Please fix the errors below."
        messages.error(request, msg)
        return self.get_context_and_render(request, form, formset, pk=pk)


class SampleDelete(LoginRequiredMixin, TemplateView):

    """
    Sample delete page.
    """
    login_url = LOGIN_URL
    template_name = "core/sample_delete.html"

    def get_context_data(self, pk):
        context = {
            'sample': get_object_or_404(Sample, pk=pk),
            'pk': pk,
        }
        return context

    def post(self, request, pk):
        get_object_or_404(Sample, pk=pk).delete()
        msg = "Successfully deleted the Sample."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('core:sample_list'))


#============================
# Library views
#----------------------------
class LibraryList(LoginRequiredMixin, TemplateView):

    """
    Library list base class.
    """
    login_url = LOGIN_URL
    class Meta:
        abstract = True

    template_name = "core/library_list.html"

    def get_context_data(self):
        context = {
            'libraries': self.library_class.objects.all().order_by(self.order),
            'library_type': self.library_type,
        }
        return context


class DlpLibraryList(LibraryList):

    """
    List of DLP libraries.
    """

    order = 'pool_id'
    library_class = DlpLibrary
    library_type = 'dlp'


class PbalLibraryList(LibraryList):

    """
    List of PBAL libraries.
    """

    order = 'sample_id'
    library_class = PbalLibrary
    library_type = 'pbal'


class TenxLibraryList(LibraryList):

    """
    List of 10x libraries.
    """

    order = 'sample_id'
    library_class = TenxLibrary
    library_type = 'tenx'


class LibraryDetail(LoginRequiredMixin, TemplateView):

    """
    Library detail base class.
    """
    login_url = LOGIN_URL
    class Meta:
        abstract = True

    template_name = "core/library_detail.html"

    def get_context_and_render(self, request, library, library_type, analyses=None, sublibinfo_fields=None, chip_metadata=None, metadata_fields=None):
        library_dict = self.sort_library_order(library)
        context = {
            'library': library,
            'library_type': library_type,
            'analyses': analyses,
            'sublibinfo_fields': sublibinfo_fields,
            'chip_metadata': chip_metadata,
            'metadata_fields': metadata_fields,
            'library_dict':library_dict,
        }
        return render(request, self.template_name, context)

    def get(self, request, pk):
        library = get_object_or_404(self.library_class, pk=pk)
        library_type = self.library_type
        return self.get_context_and_render(request, library, library_type)

    def sort_library_order(self,library):
            return library.get_field_values()


class DlpLibraryDetail(LibraryDetail):

    """
    DLP library detail page.
    """

    def get(self, request, pk):
        library = get_object_or_404(DlpLibrary, pk=pk)
        library_type = 'dlp'
        analyses = DlpAnalysisInformation.objects.filter(sequencings__in=library.dlpsequencing_set.all()).distinct()
        sublibinfo = SublibraryInformation()
        fields = MetadataField.objects.distinct().filter(chipregionmetadata__chip_region__library=library).values_list('field', flat=True).distinct()
        metadata_dict = collections.OrderedDict()

        for chip_region in library.chipregion_set.all().order_by('region_code'):
            metadata_set = chip_region.chipregionmetadata_set.all()
            d1 = {}

            for metadata in metadata_set:
                d1[metadata.metadata_field.field] = metadata.metadata_value
            row = []

            for field in fields:
                # Check that columns named in "fields" exist, else populate with "" if no entry in row for that particular metadata column
                # then adding it to a metadata dictionary with other rows
                if field not in d1.keys():
                    d1[field] = ""
                row.append(d1[field])
            metadata_dict[chip_region.region_code] = row

        return self.get_context_and_render(request, library, library_type, analyses, sublibinfo.get_fields(), metadata_dict, fields)

    def sort_library_order(self, library):
        new_library_order = ['Description', 'Result', 'Title', 'Jira ticket', 'Quality', 'Chip ID', 'Number of sublibraries']
        sorted_library_dict = OrderedDict()
        library_dict_original = dict(library.get_field_values())
        for x in new_library_order:
            sorted_library_dict[x] = library_dict_original[x]
        return sorted_library_dict


class PbalLibraryDetail(LibraryDetail):

    """
    PBAL library detail page.
    """

    library_class = PbalLibrary
    library_type = 'pbal'
    # sisyphus integration not implemented yet for pbal
    # analyses = AnalysisInformation.objects.filter(sequencings__in=library.pbalsequencing_set.all()).distinct()


class TenxLibraryDetail(LibraryDetail):

    """
    10x library detail page.
    """

    library_class = TenxLibrary
    library_type = 'tenx'
    # sisyphus integration not implemented yet for 10x
    # analyses = AnalysisInformation.objects.filter(sequencings__in=library.tenxsequencing_set.all()).distinct()

    def get(self, request, pk):
        library = get_object_or_404(TenxLibrary, pk=pk)
        library_type = 'tenx'

        fields = (
            'Experimental_condition',
            'Enzyme',
            'Digestion_Temperature',
            'Live/Dead',
            'Cells_Targeted',
        )
        metadata_dict = collections.OrderedDict()

        for condition in library.tenxcondition_set.all():
            condition_fields = condition.get_field_values()

            metadata_dict[condition.condition_id] = (
                [condition_fields[field] for field in fields])

        return self.get_context_and_render(
            request=request,
            library=library,
            library_type=library_type,
            chip_metadata=metadata_dict,
            metadata_fields=fields,
        )


class TenxConditionsDelete(LoginRequiredMixin, View):
    """Delete 10x library conditions metadata."""
    login_url = LOGIN_URL

    def post(self, request, pk):
        """Delete the 10x library's conditions."""
        library = get_object_or_404(TenxLibrary, pk=pk)
        library.tenxcondition_set.all().delete()

        msg = "Successfully deleted the the conditions metadata."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('tenx:library_detail', kwargs=dict(pk=pk)))


class LibraryDelete(LoginRequiredMixin, TemplateView):

    """
    Library delete base class.
    """
    login_url = LOGIN_URL
    class Meta:
        abstract = True

    template_name = "core/library_delete.html"

    def get_context_data(self, pk):
        context = {
            'library': get_object_or_404(self.library_class, pk=pk),
            'pk': pk,
            'library_type': self.library_type,
        }
        return context

    def post(self, request, pk):
        get_object_or_404(self.library_class, pk=pk).delete()
        msg = "Successfully deleted the Library."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse(self.library_type + ':library_list'))


class DlpLibraryDelete(LibraryDelete):

    """
    DLP library delete page.
    """

    library_class = DlpLibrary
    library_type = 'dlp'


class PbalLibraryDelete(LibraryDelete):

    """
    PBAL library delete page.
    """

    library_class = PbalLibrary
    library_type = 'pbal'


class TenxLibraryDelete(LibraryDelete):

    """
    10x library delete page.
    """

    library_class = TenxLibrary
    library_type = 'tenx'


class JiraTicketConfirm(LoginRequiredMixin, TemplateView):

    login_url = LOGIN_URL

    template_name = 'core/jira_ticket_confirm.html'

    def get(self, request):
        projects = get_projects(request.session['jira_user'], request.session['jira_password'])
        form = JiraConfirmationForm()
        #Set default values for DLP and TenX Library Ticket Creation
        #If default value can't be found, no error will be thrown, and the field will just be empty by default
        if(request.session['library_type'] == 'dlp'):
            form.fields['title'].initial = '{} - {} - {}'.format(request.session['sample_id'], request.session['pool_id'], request.session['additional_title'])
            form.fields['description'].initial = generate_dlp_jira_description(request.session['description'], request.session['library_id'])
            form.fields['reporter'].initial = 'elaks'                                                                                    
        elif(request.session['library_type'] == 'tenx'):
            form.fields['title'].initial = '{} - {}'.format(request.session['sample_id'], request.session['additional_title'])
            form.fields['description'].initial = 'Awaiting first sequencing...'
            form.fields['reporter'].initial = 'coflanagan'

        form.fields['project'].choices = [(str(project.id), project.name) for project in projects]
        form.fields['project'].initial = get_project_id_from_name(request.session['jira_user'], request.session['jira_password'], 'Single Cell')
        context = {
            'form': form,
            'library_type': request.session['library_type']
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = JiraConfirmationForm(request.POST)
        projects = get_projects(request.session['jira_user'], request.session['jira_password'])
        form.fields['project'].choices = [(str(project.id), project.name) for project in projects]
        if form.is_valid():
            try:
                new_issue = create_ticket(username=request.session['jira_user'],
                      password=request.session['jira_password'],
                      project=form['project'].value(),
                      title=form['title'].value(),
                      description=form['description'].value(),
                      reporter=form['reporter'].value(),
                    )
            except JIRAError as e:
                #Do Something
                error_message = "Failed to create the Jira Ticket. {}".format(e.text)
                messages.error(request, error_message)
                return render(request, self.template_name)
            if(request.session['library_type'] == 'dlp'):
                library = DlpLibrary.objects.get(id=request.session['library_id'])
                library.jira_ticket = new_issue
                library.save()
            elif(request.session['library_type'] == 'tenx'):
                library = TenxLibrary.objects.get(id=request.session['library_id'])
                library.jira_ticket = new_issue
                library.save()
            return HttpResponseRedirect('/{}/library/{}'.format(request.session['library_type'], library.id))


class LibraryCreate(LoginRequiredMixin, TemplateView):

    """
    Library create base class.
    """
    login_url = LOGIN_URL

    class Meta:
        abstract = True

    template_name = "core/library_create.html"

    def get_context_data(self, pk=None):
        if pk:
            sample = get_object_or_404(Sample, pk=pk)
        else:
            sample = None

        context = {
            'lib_form': self.lib_form_class(),
            'sublib_form': SublibraryForm(),
            'libdetail_formset': self.libdetail_formset_class(),
            'libcons_formset': self.libcons_formset_class(),
            'libqs_formset': self.libqs_formset_class(),
            'projects': Project.objects.all(),
            'sample': str(sample),
            'sample_id': pk,
            'related_dlp_libs': DlpLibrary.objects.all(),
            'related_tenx_libs': TenxLibrary.objects.all(),
            'library_type': self.library_type,
        }
        return context

    def get(self, request, pk=None):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        context = self.get_context_data(pk)
        return self._post(request, context)

    def _post(self, request, context, library=None, create=False):

        lib_form = self.lib_form_class(request.POST, instance=library)
        sublib_form = SublibraryForm(request.POST, request.FILES or None)
        context['lib_form'] = lib_form
        context['sublib_form'] = sublib_form

        error_message = ''
        try:
            with transaction.atomic():
                if lib_form.is_valid() and sublib_form.is_valid():
                    instance = lib_form.save(commit=False)
                    if instance.pk is None:
                        create = True
                    all_valid, formsets = self._validate_formsets(request, instance)
                    context.update(formsets)
                    if all_valid and create:
                        if context['library_type'] != 'pbal':
                            jira_user = lib_form['jira_user'].value()
                            jira_password = lib_form['jira_password'].value()
                            additional_title = lib_form['additional_title'].value()

                        #Add these fields into Session so the JiraTicketConfirm View can access them
                        if(context['library_type'] == 'pbal' or validate_credentials(jira_user, jira_password)):
                            #For DLP Libaries
                            if(context['library_type'] == 'dlp'):
                                request.session['pool_id'] = str(instance.pool_id)
                                request.session['description'] = instance.description
                            elif(context['library_type'] == 'tenx'):
                                request.session['pool'] = request.POST['tenxlibraryconstructioninformation-0-pool']
                            if context['library_type'] != 'pbal':
                                request.session['jira_user'] = jira_user
                                request.session['jira_password'] = jira_password
                                request.session['additional_title'] = additional_title
                                request.session['sample_id'] = instance.sample.sample_id
                                request.session['library_type'] = context['library_type']
                        else:
                            messages.error(request, 'Invalid Jira Credentials')
                            return render(request, self.template_name, context)
                        # Save the library
                        instance.save()
                        request.session['library_id'] = instance.id
                        # Save 10x conditions
                        if context['library_type'] == 'tenx':
                            condition_formset = TenxConditionFormset(request.POST)

                            # Save each condition
                            idx = 1
                            for condition_form in condition_formset:
                                # If a condition_form was left blank,
                                # skip it
                                if not condition_form.has_changed():
                                    continue

                                # Save the condition
                                condition = condition_form.save(commit=False)
                                condition.condition_id = idx
                                condition.library = instance
                                condition.sample = instance.sample
                                condition.save()

                                # Increment the index counter
                                idx += 1

                        # save the ManyToMany field.
                        lib_form.save_m2m()
                        # Add information from SmartChipApp files
                        region_metadata = sublib_form.cleaned_data.get('smartchipapp_region_metadata')
                        sublib_results = sublib_form.cleaned_data.get('smartchipapp_results')
                        if region_metadata is not None and sublib_results is not None:
                            instance.sublibraryinformation_set.all().delete()
                            instance.chipregion_set.all().delete()
                            create_sublibrary_models(instance, sublib_results, region_metadata)
                        # save the formsets.
                        [formset.save() for formset in formsets.values()]
                        if context["library_type"] == "pbal":
                            return HttpResponseRedirect(instance.get_absolute_url())
                        else:
                            return HttpResponseRedirect(reverse('{}:jira_ticket_confirm'.format(context['library_type'])))
                    elif all_valid and not create:
                        instance.save()
                        if context['library_type'] == 'tenx':
                            condition_formset = TenxConditionFormset(request.POST)

                            # Save each condition
                            idx = 1
                            for condition_form in condition_formset:
                                # If a condition_form was left blank,
                                # skip it
                                if not condition_form.has_changed():
                                    continue

                                # Save the condition
                                condition = condition_form.save(commit=False)
                                condition.condition_id = idx
                                condition.library = instance
                                condition.sample = instance.sample
                                condition.save()

                                # Increment the index counter
                                idx += 1

                        # save the ManyToMany field.
                        lib_form.save_m2m()
                        # Add information from SmartChipApp files
                        region_metadata = sublib_form.cleaned_data.get('smartchipapp_region_metadata')
                        sublib_results = sublib_form.cleaned_data.get('smartchipapp_results')
                        if region_metadata is not None and sublib_results is not None:
                            instance.sublibraryinformation_set.all().delete()
                            instance.chipregion_set.all().delete()
                            create_sublibrary_models(instance, sublib_results, region_metadata)
                        # save the formsets.
                        [formset.save() for formset in formsets.values()]
                        return HttpResponseRedirect('/{}/library/{}'.format(context['library_type'], instance.id))
                else:
                    messages.info(request, lib_form.errors)
                    return HttpResponseRedirect(request.get_full_path())


        except ValueError as e:
            #Can't join into a string when some args are ints, so convert them first
            for arg in e.args:
                if(type(arg) is int):
                    arg = str(arg)
                error_message += arg.encode('ascii', 'ignore') + ' '
            error_message = "Failed to create the library. " + error_message + ". Please fix the errors below."
            messages.error(request, error_message)
            return render(request, self.template_name, context)

    def _validate_formsets(self, request, instance):
        all_valid = True
        formsets = {
            'libdetail_formset': self.libdetail_formset_class(
                request.POST,
                instance=instance,
            ),
            'libcons_formset': self.libcons_formset_class(
                request.POST,
                instance=instance,
            ),
            'libqs_formset': self.libqs_formset_class(
                request.POST,
                request.FILES or None,
                instance=instance,
            ),
        }
        for k, formset in formsets.items():
            if not formset.is_valid():
                all_valid = False
            formsets[k] = formset
        return all_valid, formsets


class DlpLibraryCreate(LibraryCreate):

    """
    DLP library create page.
    """

    lib_form_class = DlpLibraryForm
    libdetail_formset_class = DlpLibrarySampleDetailInlineFormset
    libcons_formset_class = DlpLibraryConstructionInfoInlineFormset
    libqs_formset_class = DlpLibraryQuantificationAndStorageInlineFormset
    library_type = 'dlp'


class PbalLibraryCreate(LibraryCreate):

    """
    PBAL library create page.
    """

    lib_form_class = PbalLibraryForm
    libdetail_formset_class = PbalLibrarySampleDetailInlineFormset
    libcons_formset_class = PbalLibraryConstructionInfoInlineFormset
    libqs_formset_class = PbalLibraryQuantificationAndStorageInlineFormset
    library_type = 'pbal'


class TenxLibraryCreate(LibraryCreate):

    """
    10x library create page.
    """

    lib_form_class = TenxLibraryForm
    libdetail_formset_class = TenxLibrarySampleDetailInlineFormset
    libcons_formset_class = TenxLibraryConstructionInfoInlineFormset
    libqs_formset_class = TenxLibraryQuantificationAndStorageInlineFormset
    library_type = 'tenx'


    def get_context_data(self, pk=None):
        """Add in 10x condition forms."""
        context = super(TenxLibraryCreate, self).get_context_data(pk)

        context['tenx_condition_formset'] = TenxConditionFormset(
            queryset=TenxCondition.objects.none())

        return context


class LibraryUpdate(LibraryCreate):

    """
    Library update base class.
    """

    class Meta:
        abstract = True

    template_name = "core/library_update.html"

    def get_context_data(self, pk):
        library = get_object_or_404(self.library_class, pk=pk)
        selected_projects = [p.name for p in library.projects.all()]
        selected_related_dlp_libs = library.relates_to_dlp.all()
        selected_related_tenx_libs = library.relates_to_tenx.all()

        context = {
            'pk': pk,
            'lib_form': self.lib_form_class(instance=library),
            'sublib_form': SublibraryForm(),
            'libdetail_formset': self.libdetail_formset_class(instance=library),
            'libcons_formset': self.libcons_formset_class(instance=library),
            'libqs_formset': self.libqs_formset_class(instance=library),
            'projects': Project.objects.all(),
            'selected_projects': selected_projects,
            'related_dlp_libs': DlpLibrary.objects.all(),
            'related_tenx_libs': TenxLibrary.objects.all(),
            'selected_related_dlp_libs': selected_related_dlp_libs,
            'selected_related_tenx_libs': selected_related_tenx_libs,
            'library_type': self.library_type,
        }
        return context

    def post(self, request, pk, create=False):
        context = self.get_context_data(pk)
        library = get_object_or_404(self.library_class, pk=pk)
        return self._post(request, context, library=library)


class DlpLibraryUpdate(LibraryUpdate):

    """
    DLP library update page.
    """

    library_class = DlpLibrary
    lib_form_class = DlpLibraryForm
    libdetail_formset_class = DlpLibrarySampleDetailInlineFormset
    libcons_formset_class = DlpLibraryConstructionInfoInlineFormset
    libqs_formset_class = DlpLibraryQuantificationAndStorageInlineFormset
    library_type = 'dlp'


class PbalLibraryUpdate(LibraryUpdate):

    """
    PBAL library update page.
    """

    library_class = PbalLibrary
    lib_form_class = PbalLibraryForm
    libdetail_formset_class = PbalLibrarySampleDetailInlineFormset
    libcons_formset_class = PbalLibraryConstructionInfoInlineFormset
    libqs_formset_class = PbalLibraryQuantificationAndStorageInlineFormset
    library_type = 'pbal'


class TenxLibraryUpdate(LibraryUpdate):

    """
    10x library update page.
    """

    library_class = TenxLibrary
    lib_form_class = TenxLibraryForm
    libdetail_formset_class = TenxLibrarySampleDetailInlineFormset
    libcons_formset_class = TenxLibraryConstructionInfoInlineFormset
    libqs_formset_class = TenxLibraryQuantificationAndStorageInlineFormset
    library_type = 'tenx'

    def get_context_data(self, pk=None):
        """Add in 10x condition forms."""
        context = super(TenxLibraryUpdate, self).get_context_data(pk)

        library = get_object_or_404(self.library_class, pk=pk)
        context['tenx_condition_formset'] = TenxConditionFormset(
            queryset=library.tenxcondition_set.all())

        return context


#============================
# Project views
#----------------------------
class ProjectList(LoginRequiredMixin, TemplateView):

    """
    Project detail page.
    """
    login_url = LOGIN_URL
    template_name = "core/project_list.html"

    def get_context_data(self):
        context = {
            'projects': Project.objects.all().order_by('name'),
        }
        return context

class ProjectDetail(TemplateView):

    template_name = "core/project_detail.html"

    def get_context_data(self, pk):
        context = {
            'project': get_object_or_404(Project, pk=pk),
        }
        return context


class ProjectDelete(LoginRequiredMixin, TemplateView):

    """
    Project delete page.
    """
    login_url = LOGIN_URL
    template_name = "core/project_delete.html"

    def get_context_data(self, pk):
        context = {
            'project': get_object_or_404(Project, pk=pk),
            'pk': pk,
        }
        return context

    def post(self, request, pk):
        get_object_or_404(Project, pk=pk).delete()
        msg = "Successfully deleted the Project."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('core:project_list'))


class ProjectCreate(LoginRequiredMixin,TemplateView):

    """
    Project create page.
    """
    login_url = LOGIN_URL
    template_name = "core/project_create.html"

    def get_context_data(self):
        context = {
            'form': ProjectForm(),
        }
        return context

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            instance = form.save()
            msg = "Successfully created the %s project." % instance.name
            messages.success(request, msg)
            return HttpResponseRedirect(instance.get_absolute_url())


class ProjectUpdate(LoginRequiredMixin, TemplateView):

    """
    Project update page.
    """
    login_url = LOGIN_URL
    template_name = "core/project_update.html"

    def get_context_data(self, pk):
        context = {
            'pk': pk,
            'form': ProjectForm(instance=get_object_or_404(Project, pk=pk)),
        }
        return context

    def post(self, request, pk):
        form = ProjectForm(request.POST, instance=get_object_or_404(Project, pk=pk))
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            msg = "Successfully updated the Project."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.get_absolute_url())


#============================
# Sequencing views
#----------------------------
class SequencingList(LoginRequiredMixin, TemplateView):

    """
    Sequencing list base class.
    """
    login_url = LOGIN_URL
    class Meta:
        abstract = True

    template_name = "core/sequencing_list.html"

    def get_context_data(self):

        sequencing_list = self.sequencing_class.objects.all().order_by('library')
        for sequencing in sequencing_list:
            try:
                sequencing.most_recent_lane = sequencing.dlplane_set.order_by('-id')[0].sequencing_date.strftime('%b. %d, %Y')
            except IndexError:
                sequencing.most_recent_lane = None
            except AttributeError:
                sequencing.most_recent_lane = None

        context = {
            'sequencings': sequencing_list,
            'library_type': self.library_type,
        }
        
        return context


class DlpSequencingList(SequencingList):

    """
    List of DLP sequencings.
    """

    sequencing_class = DlpSequencing
    library_type = 'dlp'


class PbalSequencingList(SequencingList):

    """
    List of PBAL sequencings.
    """

    sequencing_class = PbalSequencing
    library_type = 'pbal'


class TenxSequencingList(SequencingList):

    """
    List of 10x sequencings.
    """

    sequencing_class = TenxSequencing
    library_type = 'tenx'


class SequencingDetail(LoginRequiredMixin, TemplateView):

    """
    Sequencing detail base class.
    """
    login_url = LOGIN_URL
    class Meta:
        abstract = True

    template_name = "core/sequencing_detail.html"

    def get(self, request, pk):
        key = "gsc_form_metadata_%s" % pk
        download = False
        if key in request.session.keys():
            download = True

        context = {
            'sequencing': get_object_or_404(self.sequencing_class, pk=pk),
            'download': download,
            'library_type': self.library_type,
        }
        return render(request, self.template_name, context)


class DlpSequencingDetail(SequencingDetail):

    """
    DLP sequencing detail page.
    """

    sequencing_class = DlpSequencing
    library_type = 'dlp'


class PbalSequencingDetail(SequencingDetail):

    """
    DLP sequencing detail page.
    """

    sequencing_class = PbalSequencing
    library_type = 'pbal'


class TenxSequencingDetail(SequencingDetail):

    """
    10x sequencing detail page.
    """

    sequencing_class = TenxSequencing
    library_type = 'tenx'


class AddWatchers(LoginRequiredMixin, TemplateView):

    login_url = LOGIN_URL
    template_name = "core/add_watchers.html"

    def get(self, request):
        if request.session['library_type'] == 'dlp':
            #Set initial checkboxes to every Jira User associated with DLP
            form = AddWatchersForm(initial={'watchers': list(JiraUser.objects.filter(associated_with_dlp=True).values_list('username', flat=True))})
            form.fields['comment'].initial = "A new Sequencing has been created and awaits {} lanes".format(request.session['number_of_lanes_requested'])
        elif request.session['library_type'] == 'tenx':
            form = AddWatchersForm(initial={'watchers': list(JiraUser.objects.filter(associated_with_tenx=True).values_list('username', flat=True))})
            form.fields['comment'].initial = "A new Sequencing has been created and awaits {} lanes".format(request.session['number_of_lanes_requested'])  
        else:
            form = AddWatchersForm()
        context = {
            'form': form,
            'library_type': request.session['library_type'],
            'jira_ticket': request.session['jira_ticket'],
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AddWatchersForm(request.POST)
        if form.is_valid():
            if request.session['library_type'] == 'tenx':
                reference_genome = get_reference_genome_from_sample_id(request.session['sample_id'])
                updated_description = generate_tenx_jira_description(request.session['sequencing_center'], reference_genome, request.session['pool_id'])
                try:
                    update_description(request.session['jira_user'], request.session['jira_password'], request.session['jira_ticket'], updated_description)
                except JIRAError as e:
                    msg = e.text
                    messages.error(request, msg)
                    return self.get(request)
            try:
                add_watchers(request.session['jira_user'], request.session['jira_password'], request.session['jira_ticket'], form.cleaned_data['watchers'])
                add_jira_comment(request.session['jira_user'], request.session['jira_password'], request.session['jira_ticket'], form.cleaned_data['comment'])
            except JIRAError as e:
                msg = e.text
                messages.error(request, msg)
                return self.get(request)
        return HttpResponseRedirect('/{}/sequencing/{}'.format(request.session['library_type'], request.session['sequencing_id']))



class SequencingCreate(LoginRequiredMixin, TemplateView):

    """
    Sequencing create base class.
    """
    login_url = LOGIN_URL
    class Meta:
        abstract = True

    template_name = "core/sequencing_create.html"

    def get_context_and_render(self, request, from_library, form):
        if from_library:
            library = get_object_or_404(self.library_class, pk=from_library)
        else:
            library = None

        context = {
            'form': form,
            'library': str(library),
            'library_id': from_library,
            'related_seqs': self.sequencing_class.objects.all(),
            'library_type': self.library_type,
        }
        return render(request, self.template_name, context)

    def get(self, request, from_library=None):
        form = self.form_class()
        return self.get_context_and_render(request, from_library, form)

    def post(self, request, from_library=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            library = instance.library
            if(validate_credentials(form.cleaned_data['jira_user'], form.cleaned_data['jira_password'])):
                request.session['jira_user'] = form.cleaned_data['jira_user']
                request.session['jira_password'] = form.cleaned_data['jira_password']
                request.session['jira_ticket'] = library.jira_ticket
                request.session['library_type'] = library.library_type
                if(library.library_type == 'tenx'):
                    request.session['pool_id'] = library.tenxlibraryconstructioninformation.pool
                request.session['sample_id'] = library.sample.sample_id
                request.session['number_of_lanes_requested'] = instance.number_of_lanes_requested
                request.session['sequencing_center'] = instance.sequencing_center
            else:
                messages.error(request, 'Invalid Jira Credentials')
                return self.get_context_and_render(request, from_library, form)

            instance.save()
            request.session['sequencing_id'] = instance.id
            #form.save_m2m()
            msg = "Successfully created the Sequencing."
            messages.success(request, msg)
            return HttpResponseRedirect(reverse('{}:add_watchers'.format(library.library_type)))
        else:
            msg = "Failed to create the sequencing. Please fix the errors below."
            messages.error(request, msg)
            return self.get_context_and_render(request, from_library, form)


class DlpSequencingCreate(SequencingCreate):

    """
    DLP sequencing create page.
    """

    library_class = DlpLibrary
    sequencing_class = DlpSequencing
    form_class = DlpSequencingForm
    library_type = 'dlp'


class PbalSequencingCreate(SequencingCreate):

    """
    PBAL sequencing create page.
    """

    library_class = PbalLibrary
    sequencing_class = PbalSequencing
    form_class = PbalSequencingForm
    library_type = 'pbal'


class TenxSequencingCreate(SequencingCreate):

    """
    10x sequencing create page.
    """

    library_class = TenxLibrary
    sequencing_class = TenxSequencing
    form_class = TenxSequencingForm
    library_type = 'tenx'


class SequencingUpdate(LoginRequiredMixin, TemplateView):

    """
    Sequencing update base class.
    """
    login_url = LOGIN_URL
    class Meta:
        abstract = True

    template_name = "core/sequencing_update.html"

    def get_context_and_render(self, request, sequencing, form):
        context = {
            'pk': sequencing.pk,
            'form': form,
            'related_seqs': self.sequencing_class.objects.all(),
            'selected_related_seqs': sequencing.relates_to.only(),
            'library_type': self.library_type,
        }
        return render(request, self.template_name, context)

    def get(self, request, pk):
        sequencing = get_object_or_404(self.sequencing_class, pk=pk)
        form = self.form_class(instance=sequencing)
        return self.get_context_and_render(request, sequencing, form)

    def post(self, request, pk):
        sequencing = get_object_or_404(self.sequencing_class, pk=pk)
        old_count = sequencing.number_of_lanes_requested
        form = self.form_class(request.POST, instance=sequencing)
        if form.is_valid():
            instance = form.save(commit=False)
            #Don't require JIRA integration if not updating the number of lanes field
            if(old_count != instance.number_of_lanes_requested):
                jira_comment = "Sequencing Goal has been updated from {} to {} for this [Sequencing|http://colossus.bcgsc.ca/{}/sequencing/{}]".format(old_count, instance.number_of_lanes_requested, self.library_type, pk)
                try:
                    add_jira_comment(
                        form.cleaned_data['jira_user'],
                        form.cleaned_data['jira_password'],
                        instance.library.jira_ticket,
                        jira_comment
                    )
                except JIRAError as e:
                    msg = "JIRA Error: {}".format(e.response.reason)
                    messages.error(request, msg)
                    return self.get_context_and_render(request, sequencing, form)

            instance.save()
            form.save_m2m()

            msg = "Successfully updated the Sequencing."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            msg = "Failed to update the sequencing. Please fix the errors below."
            messages.error(request, msg)
            return self.get_context_and_render(request, sequencing, form)


class DlpSequencingUpdate(SequencingUpdate):

    """
    DLP sequencing update page.
    """

    sequencing_class = DlpSequencing
    form_class = DlpSequencingForm
    library_type = 'dlp'


class PbalSequencingUpdate(SequencingUpdate):

    """
    PBAL sequencing update page.
    """

    sequencing_class = PbalSequencing
    form_class = PbalSequencingForm
    library_type = 'pbal'


class TenxSequencingUpdate(SequencingUpdate):

    """
    10x sequencing update page.
    """

    sequencing_class = TenxSequencing
    form_class = TenxSequencingForm
    library_type = 'tenx'


class SequencingDelete(LoginRequiredMixin, TemplateView):

    """
    Sequencing delete base class.
    """
    login_url = LOGIN_URL
    class Meta:
        abstract = True

    template_name = "core/sequencing_delete.html"

    def get_context_data(self, pk):
        context = {
            'sequencing': get_object_or_404(self.sequencing_class, pk=pk),
            'pk': pk,
            'library_type': self.library_type,
        }
        return context

    def post(self, request, pk):
        get_object_or_404(self.sequencing_class, pk=pk).delete()
        msg = "Successfully deleted the Sequencing."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse(self.library_type + ':sequencing_list'))


class DlpSequencingDelete(SequencingDelete):

    """
    DLP sequencing delete page.
    """

    sequencing_class = DlpSequencing
    library_type = 'dlp'


class PbalSequencingDelete(SequencingDelete):

    """
    PBAL sequencing delete page.
    """

    sequencing_class = PbalSequencing
    library_type = 'pbal'


class TenxSequencingDelete(SequencingDelete):

    """
    10x sequencing delete page.
    """

    sequencing_class = TenxSequencing
    library_type = 'tenx'


@login_required
def dlp_sequencing_get_samplesheet(request, pk):

    """
    Generates downloadable samplesheet.
    """

    ofilename, ofilepath = generate_samplesheet(pk)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % ofilename
    ofile = open(ofilepath, 'r')
    response.write(ofile.read())
    ofile.close()
    os.remove(ofilepath)
    return response


@login_required
def dlp_sequencing_get_queried_samplesheet(request, flowcell):

    """
    Makes downloading samplesheets from flowcell possible.
    """

    try:
        pk = DlpLane.objects.get(flow_cell_id=flowcell).pk
        return dlp_sequencing_get_samplesheet(request, pk)
    except DlpSequencing.DoesNotExist:
        msg = "Sorry, no sequencing with flowcell {} found.".format(flowcell)
        messages.warning(request, msg)
        return HttpResponseRedirect(reverse('index'))
    except DlpSequencing.MultipleObjectsReturned:
        msg = "Multiple flowcells with ID {} found.".format(flowcell)
        messages.warning(request, msg)
        return HttpResponseRedirect(reverse('index'))


class DlpSequencingCreateGSCFormView(LoginRequiredMixin, TemplateView):

    """
    Sequencing GSC submission form.
    """
    login_url = LOGIN_URL
    template_name = "core/sequencing_create_gsc_form.html"

    def get_context_data(self, pk):
        context = {
            'pk': pk,
            'delivery_info_form': GSCFormDeliveryInfo(),
            'submitter_info_form': GSCFormSubmitterInfo(),
            'library_type': 'dlp',
        }
        return context

    def get(self, request, pk):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)

    def post(self, request, pk):
        sequencing = get_object_or_404(DlpSequencing, pk=pk)
        context = self.get_context_data(pk)
        delivery_info_form = GSCFormDeliveryInfo(request.POST)
        submitter_info_form = GSCFormSubmitterInfo(request.POST)
        if delivery_info_form.is_valid() and submitter_info_form.is_valid():
            key = "gsc_form_metadata_%s" % pk
            request.session[key] = request.POST
            msg = "Successfully started downloading the GSC submission form."
            messages.success(request, msg)
            return HttpResponseRedirect(sequencing.get_absolute_url())
        else:
            context['delivery_info_form'] = delivery_info_form
            context['submitter_info_form'] = submitter_info_form
            msg = "please fix the errors below."
            messages.error(request, msg)
        return render(request, self.template_name, context)


@login_required
def dlp_sequencing_get_gsc_form(request, pk):

    """
    Generates downloadable GSC submission form.
    """
    key = "gsc_form_metadata_%s" % pk
    metadata = request.session.pop(key)
    ofilename, ofilepath = generate_gsc_form(pk, metadata)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % ofilename
    ofile = open(ofilepath, 'r')
    response.write(ofile.read())
    ofile.close()
    os.remove(ofilepath)
    return response


#============================
# Lane views
#----------------------------
class LaneCreate(LoginRequiredMixin, TemplateView):

    """
    Lane create page.
    """
    login_url = LOGIN_URL
    template_name = "core/lane_create.html"

    def get_context_and_render(self, request, from_sequencing, form):
        if from_sequencing:
            sequencing = get_object_or_404(self.sequencing_class, pk=from_sequencing)
        else:
            sequencing = None

        context = {
            'form': form,
            'sequencing': str(sequencing),
            'sequencing_id': from_sequencing,
            'library_type': self.library_type,
        }
        return render(request, self.template_name, context)

    def get(self, request, from_sequencing=None):
        form = self.form_class()
        return self.get_context_and_render(request, from_sequencing, form)

    def post(self, request, from_sequencing=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save()
            msg = "Successfully created the lane."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.sequencing.get_absolute_url())
        else:
            msg = "Failed to create the lane. Please fix the errors below."
            messages.error(request, msg)
            return self.get_context_and_render(request, from_sequencing, form)


class DlpLaneCreate(LaneCreate):

    """
    DLP lane create page.
    """

    sequencing_class = DlpSequencing
    form_class = DlpLaneForm
    library_type = 'dlp'


class PbalLaneCreate(LaneCreate):

    """
    PBAL lane create page.
    """

    sequencing_class = PbalSequencing
    form_class = PbalLaneForm
    library_type = 'pbal'


class TenxLaneCreate(LaneCreate):

    """
    10x lane create page.
    """

    sequencing_class = TenxSequencing
    form_class = TenxLaneForm
    library_type = 'tenx'


class LaneUpdate(LoginRequiredMixin, TemplateView):

    """
    Lane update base class.
    """
    login_url = LOGIN_URL
    class Meta:
        abstract = True

    template_name = "core/lane_update.html"

    def get_context_and_render(self, request, lane, form, pk):
        context = {
            'sequencing': lane.sequencing,
            'sequencing_id': lane.sequencing_id,
            'form': form,
            'pk': pk,
            'library_type': self.library_type,
        }
        return render(request, self.template_name, context)

    def get(self, request, pk):
        lane = get_object_or_404(self.lane_class, pk=pk)
        form = self.form_class(instance=lane)
        return self.get_context_and_render(request, lane, form, pk)

    def post(self, request, pk):
        lane = get_object_or_404(self.lane_class, pk=pk)
        form = self.form_class(request.POST, instance=lane)
        if form.is_valid():
            instance = form.save()
            msg = "Successfully updated the lane."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.sequencing.get_absolute_url())
        else:
            msg = "Failed to update the lane. Please fix the errors below."
            messages.error(request, msg)
            return self.get_context_and_render(request, lane, form, pk)


class DlpLaneUpdate(LaneUpdate):

    """
    DLP lane update page.
    """

    lane_class = DlpLane
    form_class = DlpLaneForm
    library_type = 'dlp'


class PbalLaneUpdate(LaneUpdate):

    """
    PBAL lane update page.
    """

    lane_class = PbalLane
    form_class = PbalLaneForm
    library_type = 'pbal'


class TenxLaneUpdate(LaneUpdate):

    """
    10x lane update page.
    """

    lane_class = TenxLane
    form_class = TenxLaneForm
    library_type = 'tenx'


class LaneDelete(LoginRequiredMixin, TemplateView):

    """
    Lane delete base class.
    """
    login_url = LOGIN_URL
    class Meta:
        abstract = True

    template_name = "core/lane_delete.html"

    def get_context_and_render(self, request, lane, pk, sequencing):
        context = {
            'lane': lane,
            'pk': pk,
            'sequencing_id': sequencing.id,
            'library_type': self.library_type,
        }
        return render(request, self.template_name, context)

    def get(self, request, pk):
        lane = get_object_or_404(self.lane_class, pk=pk)
        sequencing = lane.sequencing
        return self.get_context_and_render(request, lane, pk, sequencing)

    def post(self, request, pk):
        lane = get_object_or_404(self.lane_class, pk=pk)
        sequencing = lane.sequencing
        lane.delete()
        msg = "Successfully deleted the Lane."
        messages.success(request, msg)
        return HttpResponseRedirect(sequencing.get_absolute_url())


class DlpLaneDelete(LaneDelete):

    """
    DLP lane delete page.
    """

    lane_class = DlpLane
    library_type = 'dlp'


class PbalLaneDelete(LaneDelete):

    """
    PBAL lane delete page.
    """

    lane_class = PbalLane
    library_type = 'pbal'


class TenxLaneDelete(LaneDelete):

    """
    10x lane delete page.
    """

    lane_class = TenxLane
    library_type = 'tenx'


#============================
# TenxChip views
#----------------------------
class TenxChipCreate(LoginRequiredMixin, TemplateView):

    login_url = LOGIN_URL
    template_name = "core/tenx/tenxchip_create.html"

    def get_context_data(self, **kwargs):
        context = {
            "form" : TenxChipForm
        }
        return context

    def post(self, request):
        form = TenxChipForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            return render_to_response('my_template.html', {'form': form})


class TenxChipList(LoginRequiredMixin, TemplateView):

    login_url = LOGIN_URL
    template_name = "core/tenx/tenxchip_list.html"

    def get_context_data(self):
        context = {
            'chips': TenxChip.objects.all().order_by('id'),
        }
        return context


class TenxChipDetail(LoginRequiredMixin, TemplateView):

    login_url = LOGIN_URL
    template_name = "core/tenx/tenxchip_detail.html"

    def get_context_data(self, pk):
        context = {
            'chip': get_object_or_404(TenxChip, pk=pk),
            'pk': pk,
        }

        return context


class TenxChipUpdate(LoginRequiredMixin, TemplateView):

    login_url = LOGIN_URL
    template_name = "core/tenx/tenxchip_update.html"

    def get_context_data(self, pk):
        chip = get_object_or_404(TenxChip, pk=pk)
        form=TenxChipForm(instance=chip)
        context = {
            "form" : form,
            "pk" : pk
        }
        return  context

    def post(self, request, pk):
        chip = get_object_or_404(TenxChip, pk=pk)
        form = TenxChipForm(request.POST, instance=chip)

        if form.is_valid():
            form.save()
            msg = "Successfully updated the Chip."
            messages.success(request, msg)
            return HttpResponseRedirect(chip.get_absolute_url())

        msg = "Failed to update the Chip. Please fix the errors below."
        messages.error(request, msg)
        return self.get_context_and_render(request, form, pk=pk)



class TenxChipDelete(LoginRequiredMixin, TemplateView):

    login_url = LOGIN_URL
    template_name = "core/tenx/tenxchip_delete.html"

    def get_context_data(self, pk):
        context = {
            'chip': get_object_or_404(TenxChip, pk=pk),
        }
        return context

    def post(self, request, pk):
        get_object_or_404(TenxChip, pk=pk).delete()
        msg = "Successfully deleted the Chip."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('tenx:chip_list'))


#============================
# Plate views
#----------------------------
@Render("core/plate_create.html")
@login_required
def plate_create(request, from_library=None):

    """
    Plate create page.
    """

    if from_library:
        library = get_object_or_404(PbalLibrary, pk=from_library)
    else:
        library = None

    if request.method == 'POST':
        form = PlateForm(request.POST)
        if form.is_valid():
            instance = form.save()
            msg = "Successfully created the plate."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.library.get_absolute_url())
        else:
            msg = "Failed to create the plate. Please fix the errors below."
            messages.error(request, msg)
    else:
        form = PlateForm()

    context = {
        'form': form,
        'library': str(library),
        'library_id': from_library,
    }
    return context


@Render("core/plate_update.html")
@login_required
def plate_update(request, pk):

    """
    Plate update page.
    """

    plate = get_object_or_404(Plate, pk=pk)

    if request.method == 'POST':
        form = PlateForm(request.POST, instance=plate)
        if form.is_valid():
            instance = form.save()
            msg = "Successfully updated the plate."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.library.get_absolute_url())
        else:
            msg = "Failed to update the plate. Please fix the errors below."
            messages.error(request, msg)
    else:
        form = PlateForm(instance=plate)

    context = {
        'form': form,
        'library': plate.library,
        'library_id': plate.library_id,
        'pk': pk,
    }
    return context


@Render("core/plate_delete.html")
@login_required
def plate_delete(request, pk):

    """
    Plate delete page.
    """

    plate = get_object_or_404(Plate, pk=pk)
    library = plate.library

    if request.method == 'POST':
        plate.delete()
        msg = "Successfully deleted the Plate."
        messages.success(request, msg)
        return HttpResponseRedirect(library.get_absolute_url())

    context = {
        'plate': plate,
        'pk': pk,
        'library_id': library.id,
    }
    return context


#============================
# Search view
#----------------------------
@login_required
def search_view(request):
    query_str = request.GET.get('query_str')
    instance = None

    # search for samples
    if Sample.objects.filter(sample_id__iexact=query_str):
        instance = Sample.objects.filter(sample_id__iexact=query_str)[0]

    # search for dlp libraries
    elif DlpLibrary.objects.filter(pool_id__iexact=query_str):
        instance = DlpLibrary.objects.filter(pool_id__iexact=query_str)[0]

    # search for jira ticket associated with dlp library
    elif DlpLibrary.objects.filter(jira_ticket__iexact=query_str):
        instance = DlpLibrary.objects.filter(jira_ticket__iexact=query_str)[0]

    # search for jira ticket associated with tenx library
    elif TenxLibrary.objects.filter(jira_ticket__iexact=query_str):
        instance = TenxLibrary.objects.filter(jira_ticket__iexact=query_str)[0]

    if instance:
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        msg = "Sorry, no match found."
        messages.warning(request, msg)
        return HttpResponseRedirect(reverse('index'))


#============================
# Summary view
#----------------------------
@Render("core/summary.html")
@login_required
def dlp_summary_view(request):

    library_per_sample_count = {s.sample_id : s.dlplibrary_set.count() for s in Sample.objects.all()}

    sublibrary_per_sample_count = {s.sample_id : s.sublibraryinformation_set.count() for s in Sample.objects.all()}

    context ={
        'library_per_sample': library_per_sample_count,
        'sublibrary_per_sample': sublibrary_per_sample_count,
        'total_sublibs': SublibraryInformation.objects.count(),
        'total_libs': DlpLibrary.objects.count(),
        'samples':Sample.objects.all().order_by('sample_id'),
    }
    return context

@login_required
def dlp_get_filtered_sublib_count(sublibs):
    unfiltered_count = sublibs.count()

    # wells to filter out
    blankwells_count = sublibs.filter(spot_well='nan').count()

    # final count
    filtered_count = unfiltered_count - blankwells_count
    return filtered_count

@login_required
def dlp_get_cell_graph(request):

    data = []
    libs = DlpLibrary.objects.filter(dlpsequencing__isnull=False, sublibraryinformation__isnull=False).distinct()

    for lib in libs:
        lib_info = {}
        lib_info['jira_ticket'] = lib.jira_ticket
        lib_info['pool_id'] = lib.pool_id
        lib_info['count'] = dlp_get_filtered_sublib_count(lib.sublibraryinformation_set)
        lib_info['id'] = lib.pk

        for sequencing in lib.dlpsequencing_set.all():
            lib_info['submission_date'] = sequencing.submission_date
            data.append(lib_info)

    df = pd.DataFrame(data)
    # TODO: change time to just only include date
    today = str(timezone.now().strftime('%Y-%m-%d'))
    ofilename = os.path.join("cell_count-" + today + ".csv")
    output_csv_path = os.path.join(settings.MEDIA_ROOT, ofilename)
    df.to_csv(output_csv_path, index=False)


    rscript_path = os.path.join(settings.BASE_DIR, "scripts", "every_cell_count_plot.R")
    cmd = "Rscript {rscript} {input_csv} {media_dir}/output.pdf".format(rscript=rscript_path, input_csv=output_csv_path, media_dir=settings.MEDIA_ROOT)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r_stdout, r_stderr = p.communicate()
    if p.returncode != 0:
        raise Exception('cmd {} failed\nstdout:\n{}\nstderr:\n{}\n'.format(cmd, r_stdout, r_stderr))

    output_plots_path = os.path.join(settings.MEDIA_ROOT, "output.pdf")

    with open(output_plots_path, 'r') as plots_pdf:

        response = HttpResponse(plots_pdf, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % ("cell-count_" + today + ".pdf")
    os.remove(output_csv_path)
    os.remove(output_plots_path)

    return response

@login_required
def export_sublibrary_csv(request,pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Sublibrary-info.csv"'
    dlp = DlpLibrary.objects.get(id=pk)
    df = pd.DataFrame(list(dlp.sublibraryinformation_set.all().values()))
    df = df.assign(Sublibrary_information = pd.Series([x.get_sublibrary_id()for x in dlp.sublibraryinformation_set.all()], index=df.index))
    df.to_csv(response)
    return response


