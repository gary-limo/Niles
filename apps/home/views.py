# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.shortcuts import render

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
import json
from .models import DataQualityCheck
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@csrf_protect
@require_http_methods(["POST"])
def save_dq_check(request):
    try:
        # Log request details
        logger.info("=== Incoming Request Details ===")
        logger.info(f"Content Type: {request.content_type}")
        logger.info(f"Raw Body: {request.body.decode('utf-8')}")
        
        # Parse JSON data
        data = json.loads(request.body)
        
        logger.info("=== Parsed JSON Data ===")
        logger.info(json.dumps(data, indent=2))

        # Extract rule-specific details if present
        rule_details = data.get('rule_details', {})
        
        # Create new DataQualityCheck instance
        dq_check = DataQualityCheck(
            database_name=data.get('database_name'),
            schema_name=data.get('schema_name'),
            table_name=data.get('table_name'),
            column_name=data.get('column_name'),
            rule_type=data.get('rule_type'),
            # Handle rule-specific fields
            length=rule_details.get('length') if data.get('rule_type') == 'LENGTH_CHECK' else None,
            like_pattern=rule_details.get('pattern') if data.get('rule_type') == 'PATTERN_MATCHING' else None,
            custom_sql=rule_details.get('sql') if data.get('rule_type') == 'CUSTOM_SQL' else None,
            # Common fields
            execution_frequency=data.get('execution_frequency'),
            alert_recipient=data.get('alert_recipient'),
            business_critical=data.get('business_critical'),
            active_flag=int(data.get('active_flag', 1))
        )

        logger.info("=== Model Instance Data ===")
        logger.info(f"Database Name: {dq_check.database_name}")
        logger.info(f"Schema Name: {dq_check.schema_name}")
        logger.info(f"Table Name: {dq_check.table_name}")
        logger.info(f"Column Name: {dq_check.column_name}")
        logger.info(f"Rule Type: {dq_check.rule_type}")
        logger.info(f"Length: {dq_check.length}")
        logger.info(f"Like Pattern: {dq_check.like_pattern}")
        logger.info(f"Custom SQL: {dq_check.custom_sql}")
        logger.info(f"Execution Frequency: {dq_check.execution_frequency}")
        logger.info(f"Alert Recipient: {dq_check.alert_recipient}")
        logger.info(f"Business Critical: {dq_check.business_critical}")
        logger.info(f"Active Flag: {dq_check.active_flag}")
        
        # Save the instance
        dq_check.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Data Quality Check saved successfully',
            'data': {
                'id': dq_check.id,
                'database_name': dq_check.database_name,
                'rule_type': dq_check.rule_type
            }
        })
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"Raw request body: {request.body.decode('utf-8')}")
        return JsonResponse({
            'status': 'error',
            'message': f'Invalid JSON data: {str(e)}'
        }, status=400)
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Validation error: {str(e)}'
        }, status=400)
        
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}")
        logger.error(str(e))
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred'
        }, status=500)



@login_required(login_url="/login/")
@require_http_methods(["GET"])
def data_quality_view(request):
    try:
        print("=== Data Quality View Debug Info ===")
        print(f"Request Method: {request.method}")
        print(f"Request Path: {request.path}")
        print(f"User: {request.user}")
        
        # Add explicit model reference and print table name
        print(f"DEBUG: Table name in model: {DataQualityCheck._meta.db_table}")
        
        # Query with print statements
        data_quality_checks = DataQualityCheck.objects.all().order_by('-updated_at')
        print(f"DEBUG: Raw SQL query: {data_quality_checks.query}")
        print(f"DEBUG: Count of records: {data_quality_checks.count()}")
        
        # Print first record if exists
        if data_quality_checks.exists():
            first_check = data_quality_checks.first()
            print(f"DEBUG: First record: {first_check.__dict__}")
        else:
            print("DEBUG: No records found in database")
        
        context = {
            'segment': 'tables',
            'data_quality_checks': data_quality_checks
        }
        
        # Print context before rendering
        print(f"DEBUG: Context being passed to template: {context}")
        print("=== End Debug Info ===")
        
        return render(request, 'home/ui-tables.html', context)
    except Exception as e:
        print(f"ERROR in data_quality_view: {str(e)}")
        import traceback
        print(f"DEBUG: Full traceback: {traceback.format_exc()}")
        context = {'segment': 'error'}
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

