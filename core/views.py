"""
Created on May 16, 2016

@author: Jafar Taghiyar (jtaghiyar@bccrc.ca)

Updated Nov 21, 2017 by Spencer Vatrt-Watts (github.com/Spenca)
"""

import os
import collections
import subprocess


#============================
# Django imports
#----------------------------
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #, permission_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.db import transaction

import pandas as pd
from django.conf import settings
from django.utils import timezone
from itertools import chain


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
    TenxSequencing,
    DlpLane,
    PbalLane,
    TenxLane,
    SublibraryInformation,
    ChipRegion,
    ChipRegionMetadata,
    MetadataField,
    Plate
)
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
    DlpSequencingDetailInlineFormset,
    PbalSequencingForm,
    PbalSequencingDetailInlineFormset,
    TenxSequencingForm,
    TenxSequencingDetailInlineFormset,
    DlpLaneForm,
    PbalLaneForm,
    TenxLaneForm,
    GSCFormDeliveryInfo,
    GSCFormSubmitterInfo,
    ProjectForm,
    PlateForm
)
from .utils import (
    create_sublibrary_models,
    generate_samplesheet,
    generate_gsc_form,
)


#============================
# 3rd-party app imports
#----------------------------
from taggit.models import Tag


#============================
# Helpers
#----------------------------
def get_libraries(self):
    return list(chain(DlpLibrary.objects.filter(projects__name=self.name), PbalLibrary.objects.filter(projects__name=self.name), TenxLibrary.objects.filter(projects__name=self.name)))
# add a method to get the list of libraries for each project name
Tag.get_libraries = get_libraries


#============================
# Index page
#----------------------------
@Render("core/index.html")
def index_view(request):
    context = {
    'sample_size': Sample.objects.count(),
    'dlp_library_size': DlpLibrary.objects.count(),
    'dlp_sequencing_size': DlpSequencing.objects.count(),
    'pbal_library_size': PbalLibrary.objects.count(),
    'pbal_sequencing_size': PbalSequencing.objects.count(),
    'tenx_library_size': TenxLibrary.objects.count(),
    'tenx_sequencing_size': TenxSequencing.objects.count(),
    'analysisinformation_size':AnalysisInformation.objects.count(),
    'analysisrun_size':AnalysisRun.objects.count()
    }
    return context


#============================
# Sample views
#----------------------------
@Render("core/sample_list.html")
def sample_list(request):
    """list of samples."""
    samples = Sample.objects.all().order_by('sample_id')
    context = {'samples': samples}
    return context


@Render("core/sample_detail.html")
def sample_detail(request, pk):
    """sample detail page."""
    sample = get_object_or_404(Sample, pk=pk)
    library_list = ['dlp', 'pbal', 'tenx']
    context = {
        'sample': sample,
        'library_list': library_list
    }
    return context
         

@method_decorator(login_required, name='dispatch')
class SampleCreate(TemplateView):

    """"
    Sample create page.
    """

    template_name="core/sample_create.html"

    def get_context_and_render(self, request, form, formset, pk=None):
        context = {
            'pk':pk,
            'form': form,
            'formset': formset
        }
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form = SampleForm()
        formset = AdditionalSampleInfoInlineFormset()
        return self.get_context_and_render(request, form, formset)

    def post(self, request, *args, **kwargs):
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

    def get(self, request, pk, *args, **kwargs):
        sample = get_object_or_404(Sample, pk=pk)
        form=SampleForm(instance=sample)
        formset=AdditionalSampleInfoInlineFormset(instance=sample)
        return self.get_context_and_render(request, form, formset, pk=pk)

    def post(self, request, pk, *args, **kwargs):
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


@Render("core/sample_delete.html")
@login_required()
def sample_delete(request, pk):
    """sample delete page."""
    sample = get_object_or_404(Sample, pk=pk)

    if request.method == 'POST':
        sample.delete()
        msg = "Successfully deleted the Sample."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('core:sample_list'))

    context = {
        'sample': sample,
        'pk': pk
    }
    return context


#============================
# Library views
#----------------------------
@Render("core/library_list.html")
def dlp_library_list(request):
    """list of libraries."""
    libraries = DlpLibrary.objects.all().order_by('pool_id')
    context = {
        'libraries': libraries, 
        'library_type': 'dlp',
    }
    return context


@Render("core/library_list.html")
def pbal_library_list(request):
    """list of libraries."""
    libraries = PbalLibrary.objects.all().order_by('sample_id')
    context = {
        'libraries': libraries, 
        'library_type': 'pbal',
    }
    return context


@Render("core/library_list.html")
def tenx_library_list(request):
    """list of libraries."""
    libraries = TenxLibrary.objects.all().order_by('sample_id')
    context = {
        'libraries': libraries, 
        'library_type': 'tenx',
    }
    return context


@Render("core/library_detail.html")
def dlp_library_detail(request, pk):
    """library detail page."""
    library = get_object_or_404(DlpLibrary, pk=pk)
    analyses = AnalysisInformation.objects.filter(sequencings__in=library.dlpsequencing_set.all()).distinct()
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

    context = {
        'library': library,
        'sublibinfo_fields': sublibinfo.get_fields(),
        'chip_metadata': metadata_dict,
        'metadata_fields': fields,
        'analyses': analyses,
        'library_type': 'dlp',
    }
    return context


@Render("core/library_detail.html")
def pbal_library_detail(request, pk):
    """library detail page."""
    library = get_object_or_404(PbalLibrary, pk=pk)
    # sisyphus integration not implemented yet for pbal
    # analyses = AnalysisInformation.objects.filter(sequencings__in=library.pbalsequencing_set.all()).distinct()

    context = {
        'library': library,
        # 'analyses':analyses,
        'library_type': 'pbal',
    }
    return context


@Render("core/library_detail.html")
def tenx_library_detail(request, pk):
    """library detail page."""
    library = get_object_or_404(TenxLibrary, pk=pk)
    # sisyphus integration not implemented yet for 10x
    # analyses = AnalysisInformation.objects.filter(sequencings__in=library.tenxsequencing_set.all()).distinct()

    context = {
        'library': library,
        # 'analyses':analyses,
        'library_type': 'tenx',
    }
    return context


@Render("core/library_delete.html")
@login_required()
def dlp_library_delete(request, pk):
    """library delete page."""
    library = get_object_or_404(DlpLibrary, pk=pk)

    if request.method == 'POST':
        library.delete()
        msg = "Successfully deleted the Library."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('dlp:library_list'))

    context = {
        'library': library,
        'pk': pk,
        'library_type': 'dlp',
    }
    return context


@Render("core/library_delete.html")
@login_required()
def pbal_library_delete(request, pk):
    """library delete page."""
    library = get_object_or_404(PbalLibrary, pk=pk)

    if request.method == 'POST':
        library.delete()
        msg = "Successfully deleted the Library."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('pbal:library_list'))

    context = {
        'library': library,
        'pk': pk,
        'library_type': 'pbal',
    }
    return context


@Render("core/library_delete.html")
@login_required()
def tenx_library_delete(request, pk):
    """library delete page."""
    library = get_object_or_404(TenxLibrary, pk=pk)

    if request.method == 'POST':
        library.delete()
        msg = "Successfully deleted the Library."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('tenx:library_list'))

    context = {
        'library': library,
        'pk': pk,
        'library_type': 'tenx',
    }
    return context


@method_decorator(login_required, name='dispatch')
class DlpLibraryCreate(TemplateView):

    """
    Library create page.
    """

    template_name = "core/library_create.html"

    def get_context_data(self, from_sample=None):
        if from_sample:
            sample = get_object_or_404(Sample, pk=from_sample)
        else:
            sample = None
        context = {
            'lib_form': DlpLibraryForm(),
            'sublib_form': SublibraryForm(),
            'libdetail_formset': DlpLibrarySampleDetailInlineFormset(),
            'libcons_formset': DlpLibraryConstructionInfoInlineFormset(),
            'libqs_formset': DlpLibraryQuantificationAndStorageInlineFormset(),
            'projects': [t.name for t in Tag.objects.all()],
            'sample': str(sample),
            'sample_id': from_sample,
            'related_libs': DlpLibrary.objects.all(),
            'library_type': 'dlp',
        }
        return context

    def get(self, request, from_sample=None, *args, **kwargs):
        context = self.get_context_data(from_sample)
        return render(request, self.template_name, context)

    def post(self, request, from_sample=None, *args, **kwargs):
        context = self.get_context_data(from_sample)
        return self._post(request, context, *args, **kwargs)

    def _post(self, request, context, *args, **kwargs):
        # this is becaues of this django feature:
        # https://code.djangoproject.com/ticket/1130
        request.POST['projects'] = ','.join(request.POST.getlist('projects'))

        lib_form = DlpLibraryForm(request.POST, instance=kwargs.get('library', None))
        sublib_form = SublibraryForm(request.POST, request.FILES or None)
        context['lib_form'] = lib_form
        context['sublib_form'] = sublib_form

        error_message = ''
        try:
            with transaction.atomic():
                if lib_form.is_valid() and sublib_form.is_valid():
                    # if 'commit=True' when saving lib_form, then it strangely
                    # raises the following error when trying to save the
                    # ManyToMany 'Projects' field:
                    # 'LibraryForm' object has no attribute 'save_m2m'.
                    # see this: https://stackoverflow.com/questions/7083152/is-save-m2m-required-in-the-django-forms-save-method-when-commit-false
                    instance = lib_form.save(commit=False)
                    all_valid, formsets = self._validate_formsets(request, instance)
                    context.update(formsets)
                    if all_valid:
                        instance.save()
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
                        messages.success(request, "Successfully created the Library.")
                        return HttpResponseRedirect(instance.get_absolute_url())
        except ValueError as e:
            error_message = ' '.join(e.args)

        error_message = "Failed to create the library. " + error_message + ". Please fix the errors below."
        messages.error(request, error_message)
        return render(request, self.template_name, context)

    def _validate_formsets(self, request, instance):
        all_valid = True
        formsets = {
        'libdetail_formset': DlpLibrarySampleDetailInlineFormset(
            request.POST,
            instance=instance
            ),
        'libcons_formset': DlpLibraryConstructionInfoInlineFormset(
            request.POST,
            instance=instance
            ),
        'libqs_formset': DlpLibraryQuantificationAndStorageInlineFormset(
            request.POST,
            request.FILES or None,
            instance=instance
            )
        }
        for k, formset in formsets.items():
            if not formset.is_valid():
                all_valid = False
            formsets[k] = formset
        return all_valid, formsets


@method_decorator(login_required, name='dispatch')
class PbalLibraryCreate(TemplateView):

    """
    Library create page.
    """

    template_name = "core/library_create.html"

    def get_context_data(self, from_sample=None):
        if from_sample:
            sample = get_object_or_404(Sample, pk=from_sample)
        else:
            sample = None
        context = {
            'lib_form': PbalLibraryForm(),
            'libdetail_formset': PbalLibrarySampleDetailInlineFormset(),
            'libcons_formset': PbalLibraryConstructionInfoInlineFormset(),
            'libqs_formset': PbalLibraryQuantificationAndStorageInlineFormset(),
            'projects': [t.name for t in Tag.objects.all()],
            'sample': str(sample),
            'sample_id': from_sample,
            'related_libs': DlpLibrary.objects.all(),
            'library_type': 'pbal',
        }
        return context

    def get(self, request, from_sample=None, *args, **kwargs):
        context = self.get_context_data(from_sample)
        return render(request, self.template_name, context)

    def post(self, request, from_sample=None, *args, **kwargs):
        context = self.get_context_data(from_sample)
        return self._post(request, context, *args, **kwargs)

    def _post(self, request, context, *args, **kwargs):
        # this is becaues of this django feature:
        # https://code.djangoproject.com/ticket/1130
        request.POST['projects'] = ','.join(request.POST.getlist('projects'))

        lib_form = PbalLibraryForm(request.POST, instance=kwargs.get('library', None))
        context['lib_form'] = lib_form

        error_message = ''
        try:
            with transaction.atomic():
                if lib_form.is_valid():
                    # if 'commit=True' when saving lib_form, then it strangely
                    # raises the following error when trying to save the
                    # ManyToMany 'Projects' field:
                    # 'LibraryForm' object has no attribute 'save_m2m'.
                    # see this: https://stackoverflow.com/questions/7083152/is-save-m2m-required-in-the-django-forms-save-method-when-commit-false
                    instance = lib_form.save(commit=False)
                    all_valid, formsets = self._validate_formsets(request, instance)
                    context.update(formsets)
                    if all_valid:
                        instance.save()
                        # save the ManyToMany field.
                        lib_form.save_m2m()
                        # save the formsets.
                        [formset.save() for formset in formsets.values()]
                        messages.success(request, "Successfully created the Library.")
                        return HttpResponseRedirect(instance.get_absolute_url())
        except ValueError as e:
            error_message = ' '.join(e.args)

        error_message = "Failed to create the library. " + error_message + ". Please fix the errors below."
        messages.error(request, error_message)
        return render(request, self.template_name, context)

    def _validate_formsets(self, request, instance):
        all_valid = True
        formsets = {
        'libdetail_formset': PbalLibrarySampleDetailInlineFormset(
            request.POST,
            instance=instance
            ),
        'libcons_formset': PbalLibraryConstructionInfoInlineFormset(
            request.POST,
            instance=instance
            ),
        'libqs_formset': PbalLibraryQuantificationAndStorageInlineFormset(
            request.POST,
            request.FILES or None,
            instance=instance
            )
        }
        for k, formset in formsets.items():
            if not formset.is_valid():
                all_valid = False
            formsets[k] = formset
        return all_valid, formsets


@method_decorator(login_required, name='dispatch')
class TenxLibraryCreate(TemplateView):

    """
    Library create page.
    """

    template_name = "core/library_create.html"

    def get_context_data(self, from_sample=None):
        if from_sample:
            sample = get_object_or_404(Sample, pk=from_sample)
        else:
            sample = None
        context = {
            'lib_form': TenxLibraryForm(),
            'libdetail_formset': TenxLibrarySampleDetailInlineFormset(),
            'libcons_formset': TenxLibraryConstructionInfoInlineFormset(),
            'libqs_formset': TenxLibraryQuantificationAndStorageInlineFormset(),
            'projects': [t.name for t in Tag.objects.all()],
            'sample': str(sample),
            'sample_id': from_sample,
            'related_libs': DlpLibrary.objects.all(),
            'library_type': 'tenx',
        }
        return context

    def get(self, request, from_sample=None, *args, **kwargs):
        context = self.get_context_data(from_sample)
        return render(request, self.template_name, context)

    def post(self, request, from_sample=None, *args, **kwargs):
        context = self.get_context_data(from_sample)
        return self._post(request, context, *args, **kwargs)

    def _post(self, request, context, *args, **kwargs):
        # this is becaues of this django feature:
        # https://code.djangoproject.com/ticket/1130
        request.POST['projects'] = ','.join(request.POST.getlist('projects'))

        lib_form = TenxLibraryForm(request.POST, instance=kwargs.get('library', None))
        context['lib_form'] = lib_form

        error_message = ''
        try:
            with transaction.atomic():
                if lib_form.is_valid():
                    # if 'commit=True' when saving lib_form, then it strangely
                    # raises the following error when trying to save the
                    # ManyToMany 'Projects' field:
                    # 'LibraryForm' object has no attribute 'save_m2m'.
                    # see this: https://stackoverflow.com/questions/7083152/is-save-m2m-required-in-the-django-forms-save-method-when-commit-false
                    instance = lib_form.save(commit=False)
                    all_valid, formsets = self._validate_formsets(request, instance)
                    context.update(formsets)
                    if all_valid:
                        instance.save()
                        # save the ManyToMany field.
                        lib_form.save_m2m()
                        # save the formsets.
                        [formset.save() for formset in formsets.values()]
                        messages.success(request, "Successfully created the Library.")
                        return HttpResponseRedirect(instance.get_absolute_url())
        except ValueError as e:
            error_message = ' '.join(e.args)

        error_message = "Failed to create the library. " + error_message + ". Please fix the errors below."
        messages.error(request, error_message)
        return render(request, self.template_name, context)

    def _validate_formsets(self, request, instance):
        all_valid = True
        formsets = {
        'libdetail_formset': TenxLibrarySampleDetailInlineFormset(
            request.POST,
            instance=instance
            ),
        'libcons_formset': TenxLibraryConstructionInfoInlineFormset(
            request.POST,
            instance=instance
            ),
        'libqs_formset': TenxLibraryQuantificationAndStorageInlineFormset(
            request.POST,
            request.FILES or None,
            instance=instance
            )
        }
        for k, formset in formsets.items():
            if not formset.is_valid():
                all_valid = False
            formsets[k] = formset
        return all_valid, formsets


class DlpLibraryUpdate(DlpLibraryCreate):

    """
    Library update page.
    """

    template_name = "core/library_update.html"

    def get_context_data(self, pk):
        library = get_object_or_404(DlpLibrary, pk=pk)
        selected_projects = library.projects.names()
        selected_related_libs = library.relates_to.only()
        context = {
        'pk': pk,
        'lib_form': DlpLibraryForm(instance=library),
        'sublib_form': SublibraryForm(),
        'libdetail_formset': DlpLibrarySampleDetailInlineFormset(
            instance=library
            ),
        'libcons_formset': DlpLibraryConstructionInfoInlineFormset(
            instance=library
            ),
        'libqs_formset': DlpLibraryQuantificationAndStorageInlineFormset(
            instance=library
            ),
        'projects': [t.name for t in Tag.objects.all()],
        'selected_projects': selected_projects,
        'related_libs': DlpLibrary.objects.all(),
        'selected_related_libs': selected_related_libs,
        'library_type': 'dlp',
        }
        return context

    def get(self, request, pk, *args, **kwargs):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        context = self.get_context_data(pk)
        library = get_object_or_404(DlpLibrary, pk=pk)
        return self._post(request, context, *args, library=library, **kwargs)


class PbalLibraryUpdate(PbalLibraryCreate):

    """
    Library update page.
    """

    template_name = "core/library_update.html"

    def get_context_data(self, pk):
        library = get_object_or_404(PbalLibrary, pk=pk)
        selected_projects = library.projects.names()
        selected_related_libs = library.relates_to.only()
        context = {
        'pk': pk,
        'lib_form': PbalLibraryForm(instance=library),
        'libdetail_formset': PbalLibrarySampleDetailInlineFormset(
            instance=library
            ),
        'libcons_formset': PbalLibraryConstructionInfoInlineFormset(
            instance=library
            ),
        'libqs_formset': PbalLibraryQuantificationAndStorageInlineFormset(
            instance=library
            ),
        'projects': [t.name for t in Tag.objects.all()],
        'selected_projects': selected_projects,
        'related_libs': DlpLibrary.objects.all(),
        'selected_related_libs': selected_related_libs,
        'library_type': 'pbal',
        }
        return context

    def get(self, request, pk, *args, **kwargs):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        context = self.get_context_data(pk)
        library = get_object_or_404(PbalLibrary, pk=pk)
        return self._post(request, context, *args, library=library, **kwargs)


class TenxLibraryUpdate(TenxLibraryCreate):

    """
    Library update page.
    """

    template_name = "core/library_update.html"

    def get_context_data(self, pk):
        library = get_object_or_404(TenxLibrary, pk=pk)
        selected_projects = library.projects.names()
        selected_related_libs = library.relates_to.only()
        context = {
        'pk': pk,
        'lib_form': TenxLibraryForm(instance=library),
        'libdetail_formset': TenxLibrarySampleDetailInlineFormset(
            instance=library
            ),
        'libcons_formset': TenxLibraryConstructionInfoInlineFormset(
            instance=library
            ),
        'libqs_formset': TenxLibraryQuantificationAndStorageInlineFormset(
            instance=library
            ),
        'projects': [t.name for t in Tag.objects.all()],
        'selected_projects': selected_projects,
        'related_libs': DlpLibrary.objects.all(),
        'selected_related_libs': selected_related_libs,
        'library_type': 'tenx',
        }
        return context

    def get(self, request, pk, *args, **kwargs):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        context = self.get_context_data(pk)
        library = get_object_or_404(TenxLibrary, pk=pk)
        return self._post(request, context, *args, library=library, **kwargs)


#============================
# Project views
#----------------------------
@Render("core/project_list.html")
def project_list(request):
    """projects detail page."""
    projects = Tag.objects.all().order_by('name')
    context = {'projects': projects}
    return context


@Render("core/project_delete.html")
@login_required()
def project_delete(request, pk):
    """project delete page."""
    project = get_object_or_404(Tag, pk=pk)

    if request.method == 'POST':
        project.delete()
        msg = "Successfully deleted the Project."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('core:project_list'))

    context = {
        'project': project,
        'pk': pk
    }
    return context


@Render("core/project_update.html")
@login_required()
def project_update(request, pk):
    project = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            msg = "Successfully updated the Project."
            messages.success(request, msg)
            return HttpResponseRedirect(reverse('core:project_list'))
    
    else:
        form = ProjectForm(instance=project)

    context = {
        'pk': pk,
        'form': form
    }
    return context


#============================
# Sequencing views
#----------------------------
@Render("core/sequencing_list.html")
def dlp_sequencing_list(request):
    """list of sequencings."""
    sequencings = DlpSequencing.objects.all().order_by('library')
    context = {
        'sequencings': sequencings,
        'library_type': 'dlp',
    }
    return context


@Render("core/sequencing_list.html")
def pbal_sequencing_list(request):
    """list of sequencings."""
    sequencings = PbalSequencing.objects.all().order_by('library')
    context = {
        'sequencings': sequencings,
        'library_type': 'pbal',
    }
    return context


@Render("core/sequencing_list.html")
def tenx_sequencing_list(request):
    """list of sequencings."""
    sequencings = TenxSequencing.objects.all().order_by('library')
    context = {
        'sequencings': sequencings,
        'library_type': 'tenx',
    }
    return context


@Render("core/sequencing_detail.html")
def dlp_sequencing_detail(request, pk):
    """sequencing detail page."""
    sequencing = get_object_or_404(DlpSequencing, pk=pk)
    key = "gsc_form_metadata_%s" % pk
    download = False
    if key in request.session.keys():
        download = True
    context = {
        'sequencing': sequencing,
        'download': download,
        'library_type': 'dlp',
    }
    return context


@Render("core/sequencing_detail.html")
def pbal_sequencing_detail(request, pk):
    """sequencing detail page."""
    sequencing = get_object_or_404(PbalSequencing, pk=pk)
    key = "gsc_form_metadata_%s" % pk
    download = False
    if key in request.session.keys():
        download = True
    context = {
        'sequencing': sequencing,
        'download': download,
        'library_type': 'pbal',
    }
    return context


@Render("core/sequencing_detail.html")
def tenx_sequencing_detail(request, pk):
    """sequencing detail page."""
    sequencing = get_object_or_404(TenxSequencing, pk=pk)
    key = "gsc_form_metadata_%s" % pk
    download = False
    if key in request.session.keys():
        download = True
    context = {
        'sequencing': sequencing,
        'download': download,
        'library_type': 'tenx',
    }
    return context
            

@Render("core/sequencing_create.html")
@login_required()
def dlp_sequencing_create(request, from_library=None):
    """sequencing create page."""
    if from_library:
        library = get_object_or_404(DlpLibrary, pk=from_library)
    else:
        library = None
    if request.method == 'POST':
        form = DlpSequencingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            seqdetail_formset = DlpSequencingDetailInlineFormset(
                request.POST,
                instance=instance
                )
            if seqdetail_formset.is_valid():
                seqdetail_formset.save()

            msg = "Successfully created the Sequencing."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            msg = "Failed to create the sequencing. Please fix the errors below."
            messages.error(request, msg)
            seqdetail_formset = DlpSequencingDetailInlineFormset()
    
    else:
        form = DlpSequencingForm()
        seqdetail_formset = DlpSequencingDetailInlineFormset()

    context = {
        'form': form,
        'seqdetail_formset': seqdetail_formset,
        'library': str(library),
        'library_id': from_library,
        'related_seqs': DlpSequencing.objects.all(),
        'library_type': 'dlp',
    }
    return context


@Render("core/sequencing_create.html")
@login_required()
def pbal_sequencing_create(request, from_library=None):
    """sequencing create page."""
    if from_library:
        library = get_object_or_404(PbalLibrary, pk=from_library)
    else:
        library = None
    if request.method == 'POST':
        form = PbalSequencingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            seqdetail_formset = PbalSequencingDetailInlineFormset(
                request.POST,
                instance=instance
                )
            if seqdetail_formset.is_valid():
                seqdetail_formset.save()

            msg = "Successfully created the Sequencing."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            msg = "Failed to create the sequencing. Please fix the errors below."
            messages.error(request, msg)
            seqdetail_formset = PbalSequencingDetailInlineFormset()
    
    else:
        form = PbalSequencingForm()
        seqdetail_formset = PbalSequencingDetailInlineFormset()

    context = {
        'form': form,
        'seqdetail_formset': seqdetail_formset,
        'library': str(library),
        'library_id': from_library,
        'related_seqs': PbalSequencing.objects.all(),
        'library_type': 'pbal',
        }
    return context


@Render("core/sequencing_create.html")
@login_required()
def tenx_sequencing_create(request, from_library=None):
    """sequencing create page."""
    if from_library:
        library = get_object_or_404(TenxLibrary, pk=from_library)
    else:
        library = None
    if request.method == 'POST':
        form = TenxSequencingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            seqdetail_formset = TenxSequencingDetailInlineFormset(
                request.POST,
                instance=instance
                )
            if seqdetail_formset.is_valid():
                seqdetail_formset.save()

            msg = "Successfully created the Sequencing."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            msg = "Failed to create the sequencing. Please fix the errors below."
            messages.error(request, msg)
            seqdetail_formset = TenxSequencingDetailInlineFormset()
    
    else:
        form = TenxSequencingForm()
        seqdetail_formset = TenxSequencingDetailInlineFormset()

    context = {
        'form': form,
        'seqdetail_formset': seqdetail_formset,
        'library': str(library),
        'library_id': from_library,
        'related_seqs': TenxSequencing.objects.all(),
        'library_type': 'tenx',
    }
    return context


@Render("core/sequencing_update.html")
@login_required()
def dlp_sequencing_update(request, pk):
    """sequencing update page."""
    sequencing = get_object_or_404(DlpSequencing, pk=pk)
    if request.method == 'POST':
        form = DlpSequencingForm(request.POST, instance=sequencing)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            seqdetail_formset = DlpSequencingDetailInlineFormset(
                request.POST,
                instance=instance
                )                        
            if seqdetail_formset.is_valid():
                seqdetail_formset.save()

            msg = "Successfully updated the Sequencing."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            msg = "Failed to update the sequencing. Please fix the errors below."
            messages.error(request, msg)
            seqdetail_formset = DlpSequencingDetailInlineFormset(
                instance=sequencing
                )
    
    else:
        form = DlpSequencingForm(
            instance=sequencing
            )
        seqdetail_formset = DlpSequencingDetailInlineFormset(
            instance=sequencing
            )

    selected_related_seqs = sequencing.relates_to.only()
    context = {
        'pk': pk,
        'form': form,
        'seqdetail_formset': seqdetail_formset,
        'related_seqs': DlpSequencing.objects.all(),
        'selected_related_seqs': selected_related_seqs,
        'library_type': 'dlp',
        }
    return context


@Render("core/sequencing_update.html")
@login_required()
def pbal_sequencing_update(request, pk):
    """sequencing update page."""
    sequencing = get_object_or_404(PbalSequencing, pk=pk)
    if request.method == 'POST':
        form = PbalSequencingForm(request.POST, instance=sequencing)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            seqdetail_formset = PbalSequencingDetailInlineFormset(
                request.POST,
                instance=instance
            )                        
            if seqdetail_formset.is_valid():
                seqdetail_formset.save()

            msg = "Successfully updated the Sequencing."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            msg = "Failed to update the sequencing. Please fix the errors below."
            messages.error(request, msg)
            seqdetail_formset = PbalSequencingDetailInlineFormset(
                instance=sequencing
            )
    
    else:
        form = PbalSequencingForm(
            instance=sequencing
        )
        seqdetail_formset = PbalSequencingDetailInlineFormset(
            instance=sequencing
        )

    selected_related_seqs = sequencing.relates_to.only()
    context = {
        'pk': pk,
        'form': form,
        'seqdetail_formset': seqdetail_formset,
        'related_seqs': PbalSequencing.objects.all(),
        'selected_related_seqs': selected_related_seqs,
        'library_type': 'pbal',
    }
    return context


@Render("core/sequencing_update.html")
@login_required()
def tenx_sequencing_update(request, pk):
    """sequencing update page."""
    sequencing = get_object_or_404(TenxSequencing, pk=pk)
    if request.method == 'POST':
        form = TenxSequencingForm(request.POST, instance=sequencing)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            seqdetail_formset = TenxSequencingDetailInlineFormset(
                request.POST,
                instance=instance
            )                        
            if seqdetail_formset.is_valid():
                seqdetail_formset.save()

            msg = "Successfully updated the Sequencing."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            msg = "Failed to update the sequencing. Please fix the errors below."
            messages.error(request, msg)
            seqdetail_formset = TenxSequencingDetailInlineFormset(
                instance=sequencing
            )
    
    else:
        form = TenxSequencingForm(
            instance=sequencing
        )
        seqdetail_formset = TenxSequencingDetailInlineFormset(
            instance=sequencing
        )

    selected_related_seqs = sequencing.relates_to.only()
    context = {
        'pk': pk,
        'form': form,
        'seqdetail_formset': seqdetail_formset,
        'related_seqs': TenxSequencing.objects.all(),
        'selected_related_seqs': selected_related_seqs,
        'library_type': 'tenx',
    }
    return context


@Render("core/sequencing_delete.html")
@login_required()
def dlp_sequencing_delete(request, pk):
    """sequencing delete page."""
    sequencing = get_object_or_404(DlpSequencing, pk=pk)

    if request.method == 'POST':
        sequencing.delete()
        msg = "Successfully deleted the Sequencing."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('dlp:sequencing_list'))

    context = {
        'sequencing': sequencing,
        'pk': pk,
        'library_type': 'dlp',
    }
    return context


@Render("core/sequencing_delete.html")
@login_required()
def pbal_sequencing_delete(request, pk):
    """sequencing delete page."""
    sequencing = get_object_or_404(PbalSequencing, pk=pk)

    if request.method == 'POST':
        sequencing.delete()
        msg = "Successfully deleted the Sequencing."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('pbal:sequencing_list'))

    context = {
        'sequencing': sequencing,
        'pk': pk,
        'library_type': 'pbal',
    }
    return context


@Render("core/sequencing_delete.html")
@login_required()
def tenx_sequencing_delete(request, pk):
    """sequencing delete page."""
    sequencing = get_object_or_404(TenxSequencing, pk=pk)

    if request.method == 'POST':
        sequencing.delete()
        msg = "Successfully deleted the Sequencing."
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('tenx:sequencing_list'))

    context = {
        'sequencing': sequencing,
        'pk': pk,
        'library_type': 'tenx',
    }
    return context


def dlp_sequencing_get_samplesheet(request, pk):
    """generate downloadable samplesheet."""
    ofilename, ofilepath = generate_samplesheet(pk)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % ofilename
    ofile = open(ofilepath, 'r')
    response.write(ofile.read())
    ofile.close()
    os.remove(ofilepath)
    return response


def dlp_sequencing_get_queried_samplesheet(request, pool_id, flowcell):
    """ make downloading samplesheets from flowcell possible """

    try:
        pk = DlpLane.objects.get(flow_cell_id=flowcell, sequencing__library__pool_id=pool_id).pk
        return dlp_sequencing_get_samplesheet(request, pk)
    except DlpSequencing.DoesNotExist:
        msg = "Sorry, no sequencing with flowcell {} and chip id {} found.".format(flowcell, pool_id)
        messages.warning(request, msg)
        return HttpResponseRedirect(reverse('index'))


@method_decorator(login_required, name='dispatch')
class DlpSequencingCreateGSCFormView(TemplateView):

    """
    Sequencing GSC submission form.
    """

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


def dlp_sequencing_get_gsc_form(request, pk):
    """generate downloadable GSC submission form."""
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
@Render("core/lane_create.html")
@login_required()
def dlp_lane_create(request, from_sequencing=None):
    """lane create page."""
    if from_sequencing:
        sequencing = get_object_or_404(DlpSequencing, pk=from_sequencing)
    else:
        sequencing = None
    if request.method == 'POST':
        form = DlpLaneForm(request.POST)
        if form.is_valid():
            instance = form.save()
            msg = "Successfully created the lane."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.sequencing.get_absolute_url())
        else:
            msg = "Failed to create the lane. Please fix the errors below."
            messages.error(request, msg)
    else:
        form = DlpLaneForm()

    context = {
        'form': form,
        'sequencing': str(sequencing),
        'sequencing_id': from_sequencing,
        'library_type': 'dlp',
    }
    return context


@Render("core/lane_create.html")
@login_required()
def pbal_lane_create(request, from_sequencing=None):
    """lane create page."""
    if from_sequencing:
        sequencing = get_object_or_404(PbalSequencing, pk=from_sequencing)
    else:
        sequencing = None
    if request.method == 'POST':
        form = PbalLaneForm(request.POST)
        if form.is_valid():
            instance = form.save()
            msg = "Successfully created the lane."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.sequencing.get_absolute_url())
        else:
            msg = "Failed to create the lane. Please fix the errors below."
            messages.error(request, msg)
    else:
        form = PbalLaneForm()

    context = {
        'form': form,
        'sequencing': str(sequencing),
        'sequencing_id': from_sequencing,
        'library_type': 'pbal',
    }
    return context


@Render("core/lane_create.html")
@login_required()
def tenx_lane_create(request, from_sequencing=None):
    """lane create page."""
    if from_sequencing:
        sequencing = get_object_or_404(TenxSequencing, pk=from_sequencing)
    else:
        sequencing = None
    if request.method == 'POST':
        form = TenxLaneForm(request.POST)
        if form.is_valid():
            instance = form.save()
            msg = "Successfully created the lane."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.sequencing.get_absolute_url())
        else:
            msg = "Failed to create the lane. Please fix the errors below."
            messages.error(request, msg)
    else:
        form = TenxLaneForm()

    context = {
        'form': form,
        'sequencing': str(sequencing),
        'sequencing_id': from_sequencing,
        'library_type': 'tenx',
    }
    return context


@Render("core/lane_update.html")
@login_required()
def dlp_lane_update(request, pk):
    """lane update page."""
    lane = get_object_or_404(DlpLane, pk=pk)

    if request.method == 'POST':
        form = DlpLaneForm(request.POST, instance=lane)
        if form.is_valid():
            instance = form.save()
            msg = "Successfully updated the lane."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.sequencing.get_absolute_url())
        else:
            msg = "Failed to update the lane. Please fix the errors below."
            messages.error(request, msg)

    else:
        form = DlpLaneForm(instance=lane)

    context = {
        'form': form,
        'sequencing': lane.sequencing,
        'sequencing_id': lane.sequencing_id,
        'pk': pk,
        'library_type': 'dlp',
    }
    return context


@Render("core/lane_update.html")
@login_required()
def pbal_lane_update(request, pk):
    """lane update page."""
    lane = get_object_or_404(PbalLane, pk=pk)

    if request.method == 'POST':
        form = PbalLaneForm(request.POST, instance=lane)
        if form.is_valid():
            instance = form.save()
            msg = "Successfully updated the lane."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.sequencing.get_absolute_url())
        else:
            msg = "Failed to update the lane. Please fix the errors below."
            messages.error(request, msg)

    else:
        form = PbalLaneForm(instance=lane)

    context = {
        'form': form,
        'sequencing': lane.sequencing,
        'sequencing_id': lane.sequencing_id,
        'pk': pk,
        'library_type': 'pbal',
    }
    return context


@Render("core/lane_update.html")
@login_required()
def tenx_lane_update(request, pk):
    """lane update page."""
    lane = get_object_or_404(TenxLane, pk=pk)

    if request.method == 'POST':
        form = TenxLaneForm(request.POST, instance=lane)
        if form.is_valid():
            instance = form.save()
            msg = "Successfully updated the lane."
            messages.success(request, msg)
            return HttpResponseRedirect(instance.sequencing.get_absolute_url())
        else:
            msg = "Failed to update the lane. Please fix the errors below."
            messages.error(request, msg)

    else:
        form = TenxLaneForm(instance=lane)

    context = {
        'form': form,
        'sequencing': lane.sequencing,
        'sequencing_id': lane.sequencing_id,
        'pk': pk,
        'library_type': 'tenx',
    }
    return context


@Render("core/lane_delete.html")
@login_required()
def dlp_lane_delete(request, pk):
    """lane delete page."""
    lane = get_object_or_404(DlpLane, pk=pk)
    sequencing = lane.sequencing

    if request.method == 'POST':
        lane.delete()
        msg = "Successfully deleted the Lane."
        messages.success(request, msg)
        return HttpResponseRedirect(sequencing.get_absolute_url())

    context = {
        'lane': lane,
        'pk': pk,
        'sequencing_id': sequencing.id,
        'library_type': 'dlp',
    }
    return context


@Render("core/lane_delete.html")
@login_required()
def pbal_lane_delete(request, pk):
    """lane delete page."""
    lane = get_object_or_404(PbalLane, pk=pk)
    sequencing = lane.sequencing

    if request.method == 'POST':
        lane.delete()
        msg = "Successfully deleted the Lane."
        messages.success(request, msg)
        return HttpResponseRedirect(sequencing.get_absolute_url())

    context = {
        'lane': lane,
        'pk': pk,
        'sequencing_id': sequencing.id,
        'library_type': 'pbal',
    }
    return context


@Render("core/lane_delete.html")
@login_required()
def tenx_lane_delete(request, pk):
    """lane delete page."""
    lane = get_object_or_404(TenxLane, pk=pk)
    sequencing = lane.sequencing

    if request.method == 'POST':
        lane.delete()
        msg = "Successfully deleted the Lane."
        messages.success(request, msg)
        return HttpResponseRedirect(sequencing.get_absolute_url())

    context = {
        'lane': lane,
        'pk': pk,
        'sequencing_id': sequencing.id,
        'library_type': 'tenx',
    }
    return context


#============================
# Plate views
#----------------------------
@Render("core/plate_create.html")
@login_required()
def plate_create(request, from_library=None):
    """plate create page."""
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
        'library_id': from_library
    }
    return context


@Render("core/plate_update.html")
@login_required()
def plate_update(request, pk):
    """plate update page."""
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
        'pk': pk
    }
    return context


@Render("core/plate_delete.html")
@login_required()
def plate_delete(request, pk):
    """plate delete page."""
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
        'library_id': library.id
    }
    return context


#============================
# Search view
#----------------------------
def search_view(request):
    query_str = request.GET.get('query_str')
    instance = None

    # search for samples
    if Sample.objects.filter(sample_id=query_str):
        instance = Sample.objects.filter(sample_id=query_str)[0]

    # search for dlp libraries
    elif DlpLibrary.objects.filter(pool_id=query_str):
        instance = DlpLibrary.objects.filter(pool_id=query_str)[0]

    # search for jira ticket associated with dlp library
    elif DlpLibrary.objects.filter(jira_ticket=query_str):
        instance = DlpLibrary.objects.filter(jira_ticket=query_str)[0]

    # search for jira ticket associated with tenx library
    elif TenxLibrary.objects.filter(jira_ticket=query_str):
        instance = TenxLibrary.objects.filter(jira_ticket=query_str)[0]

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
def dlp_summary_view(request):

    library_per_sample_count = {s.sample_id : s.dlplibrary_set.count()
                    for s in Sample.objects.all()}

    sublibrary_per_sample_count = { s.sample_id : s.sublibraryinformation_set.count()
                                   for s in Sample.objects.all()}

    context ={
        'library_per_sample': library_per_sample_count,
        'sublibrary_per_sample': sublibrary_per_sample_count,
        'total_sublibs': SublibraryInformation.objects.count(),
        'total_libs': DlpLibrary.objects.count(),
        'samples':Sample.objects.all().order_by('sample_id')
    }

    return context


def dlp_get_filtered_sublib_count(sublibs):
    unfiltered_count = sublibs.count()

    # wells to filter out
    blankwells_count = sublibs.filter(spot_well='nan').count()

    # final count
    filtered_count = unfiltered_count - blankwells_count
    return filtered_count


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
    today = str(timezone.now().strftime('%b-%d-%Y'))
    ofilename = os.path.join("cell_count-" + today + ".csv")
    output_csv_path = os.path.join(settings.MEDIA_ROOT, ofilename)
    df.to_csv(output_csv_path, index=False)


    rscript_path = os.path.join(settings.BASE_DIR, "scripts", "every_cell_count_plot.R")
    cmd = "Rscript {rscript} {input_csv} {media_dir}/output.pdf".format(
        rscript=rscript_path, input_csv=output_csv_path, media_dir=settings.MEDIA_ROOT)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r_stdout, r_stderr = p.communicate()
    if p.returncode != 0:
        raise Exception('cmd {} failed\nstdout:\n{}\nstderr:\n{}\n'.format(cmd, r_stdout, r_stderr))

    output_plots_path = os.path.join(settings.MEDIA_ROOT,
                           "output.pdf")

    with open(output_plots_path, 'r') as plots_pdf:

        response = HttpResponse(plots_pdf, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % ("cell_count-" + today)
    os.remove(output_csv_path)
    os.remove(output_plots_path)

    return response
