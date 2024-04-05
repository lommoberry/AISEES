from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.urls import reverse
from .models import Post, Researcher, ResearchItem
from .forms import PostForm, UserAndResearcherForm, ResearchItemForm
from .tokens import account_activation_token

User = get_user_model()

def home(request):
    return render(request, 'myapp/home.html')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'myapp/post_list.html', {'posts': posts})

@staff_member_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'myapp/add_post.html', {'form': form})

def memberlist(request):
    members = Researcher.objects.all()
    return render(request, 'myapp/memberlist.html', {'members': members})

def success(request):
    return render(request, 'myapp/success.html')

@transaction.atomic
def register(request):
    if request.method == 'POST':
        form = UserAndResearcherForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            form.save_m2m()

            researcher = Researcher.objects.get(user=user)
            researcher.first_name = user.first_name
            researcher.last_name = user.last_name
            researcher.address = form.cleaned_data.get('address', '')
            researcher.position_title = form.cleaned_data.get('position_title', '')
            researcher.affiliation_institution = form.cleaned_data.get('affiliation_institution', '')
            researcher.research_interests = form.cleaned_data.get('research_interests', '')
            researcher.degree_sought = form.cleaned_data.get('degree_sought', '')
            researcher.expected_degree_date = form.cleaned_data.get('expected_degree_date', None)
            
            # For ManyToMany fields like countries_of_research_focus, ensure this is handled correctly
            if 'countries_of_research_focus' in form.cleaned_data:
                researcher.countries_of_research_focus.set(form.cleaned_data['countries_of_research_focus'])
            
            researcher.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            full_link = request.build_absolute_uri(activation_link)
            send_mail('Activate your account', f'Please use this link to activate your account: {full_link}', 'from@example.com', [user.email])
            messages.info(request, 'Please confirm your email address to complete the registration')
            return redirect('home')
    else:
        form = UserAndResearcherForm()
    return render(request, 'myapp/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
                        # Now, set email_verified to True for the researcher
            if hasattr(user, 'researcher'):
                user.researcher.email_verified = True
                user.researcher.save()
            messages.success(request, 'Your email has been verified successfully. Now you can log in.')
            return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        pass
    messages.error(request, 'The activation link was invalid or expired.')
    return redirect('home')

@staff_member_required
def upload_research_item(request):
    if request.method == 'POST':
        form = ResearchItemForm(request.POST, request.FILES)
        if form.is_valid():
            research_item = form.save(commit=False)
            research_item.uploaded_by = request.user  # Set the uploader to the current user
            research_item.save()
            form.save_m2m()  # Save many-to-many fields if your form has them
            messages.success(request, 'Research item uploaded successfully.')
            return redirect('home')  # Make sure this is the correct name of your target view
    else:
        # Provide initial data for 'uploaded_by' only when rendering the form initially
        form = ResearchItemForm(initial={'uploaded_by': request.user})
    return render(request, 'myapp/upload_research_item.html', {'form': form})
# @login_required
# def upload_research_item(request):
#     if request.method == 'POST':
#         form = ResearchItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Submitted successfully.')
#             return redirect('home')
#     else:
#         form = ResearchItemForm(initial={'uploaded_by': request.user.id})
#     return render(request, 'myapp/upload_research_item.html', {'form': form})

from django.db.models import Q
def search_research_items(request):
    query = request.GET.get('q', '')
    if query:
        # Search in various fields with OR conditions
        items = ResearchItem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(other__icontains=query) |
            Q(author__icontains=query) |
            Q(source__icontains=query) |
            Q(subject__icontains=query) |
            Q(century__icontains=query) |  # Assuming you want to allow century in query
            Q(date__icontains=query) |  # Assuming date is stored in a way that makes this query meaningful
            Q(country__name__icontains=query) |  # For ManyToMany fields like country
            Q(CE_or_BCE__icontains=query)
        ).distinct()  # `.distinct()` ensures unique results when querying ManyToMany fields
    else:
        items = ResearchItem.objects.all()
    return render(request, 'myapp/search_results.html', {'items': items, 'query': query})

# def research_item_detail(request, pk):
#     item = get_object_or_404(ResearchItem, pk=pk)
#     return render(request, 'myapp/research_item_detail.html', {'item': item})

def research_item_detail(request, pk):
    research_item = get_object_or_404(ResearchItem, pk=pk)
    return render(request, 'myapp/research_item_detail.html', {'research_item': research_item})

# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
# from django.urls import reverse_lazy, reverse
# from django.views.generic.edit import CreateView
# from django.core.mail import send_mail
# from django.core.signing import Signer, BadSignature
# from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
# from django.utils import timezone
# from django.conf import settings
# from django.contrib.auth.models import User
# from .models import Item, Post, Researcher  # Adjust User import based on your project setup
# from .forms import PostForm, UserAndResearcherForm

# # Home Page View
# def home(request):
#     return render(request, 'myapp/home.html')

# # Post List View
# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'myapp/post_list.html', {'posts': posts})

# # Add Post View
# @staff_member_required
# def add_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user  # Assuming the Post model's author field is a User.
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('home')
#     else:
#         form = PostForm()
#     return render(request, 'myapp/add_post.html', {'form': form})


# # Member List View
# def memberlist(request):
#     members = Researcher.objects.all()
#     return render(request, 'myapp/memberlist.html', {'members': members})

# # Success Page View
# def success(request):
#     return render(request, 'myapp/success.html')

# # Email Verification
# from django.core.mail import send_mail
# from django.urls import reverse
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from myapp.tokens import account_activation_token

# def send_verification_email(request, user):
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = account_activation_token.make_token(user)
#     activation_link = "{0}://{1}{2}".format(
#         request.scheme, request.get_host(),
#         reverse('activate', kwargs={'uidb64': uid, 'token': token})
#     )

#     subject = 'Activate your account'
#     message = 'Hi, please use the link to activate your account: {}'.format(activation_link)
#     from_email = 'from@yourdomain.com'
#     recipient_list = [user.email]

#     send_mail(subject, message, from_email, recipient_list)


# # Verify Email View
# from django.contrib.auth import get_user_model
# from django.http import HttpResponse
# from myapp.tokens import account_activation_token

# # User = get_user_model()

# # def activate(request, uidb64, token):
# #     try:
# #         uid = urlsafe_base64_decode(uidb64).decode()
# #         user = User.objects.get(pk=uid)
# #     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
# #         user = None

# #     if user is not None and account_activation_token.check_token(user, token):
# #         user.is_active = True
# #         user.save()
# #         # Log the user in (optional)
# #         return HttpResponse('Thank you for your email confirmation. Now you can login to your account.')
# #     else:
# #         return HttpResponse('Activation link is invalid!')

# from django.http import HttpResponse
# from django.shortcuts import redirect
# from django.contrib.auth import get_user_model
# from django.utils.http import urlsafe_base64_decode
# from django.contrib.auth.tokens import default_token_generator as token_generator

# def verify_email(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         # Optionally log the user in
#         # Log the user in (your custom logic here)
#         return HttpResponse('Your email has been verified successfully. Now you can log in.')
#     else:
#         return HttpResponse('The verification link was invalid, possibly because it has already been used.')



# from django.shortcuts import render, redirect
# from .forms import UserAndResearcherForm
# from django.contrib import messages
# from django.contrib.auth import get_user_model
# from .models import Researcher
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import get_user_model
# from django.db import transaction
# from django.utils.http import urlsafe_base64_encode, force_bytes
# from django.urls import reverse
# from .models import Researcher
# from .forms import UserAndResearcherForm
# from .tokens import account_activation_token  # Ensure you have this token generator correctly set up as previously described

# def register(request):
#     if request.method == 'POST':
#         form = UserAndResearcherForm(request.POST)
#         if form.is_valid():
#             with transaction.atomic():  # Ensure atomicity of user creation and email sending
#                 user = form.save(commit=False)
#                 user.is_active = False  # Don't activate account until email is confirmed
#                 user.save()
#                 form.save_m2m()  # Needed if your form has many-to-many fields
                
#                 # Send verification email
#                 uid = urlsafe_base64_encode(force_bytes(user.pk))
#                 token = account_activation_token.make_token(user)
#                 activation_link = "{0}://{1}{2}".format(
#                     request.scheme, request.get_host(),
#                     reverse('activate', kwargs={'uidb64': uid, 'token': token})
#                 )

#                 subject = 'Activate your account'
#                 message = 'Hi, please use the link to activate your account: {}'.format(activation_link)
#                 user.email_user(subject, message)  # Simpler way to send email to the user

#                 messages.info(request, 'Please confirm your email address to complete the registration')
#                 return redirect('home')
#     else:
#         form = UserAndResearcherForm()
#     return render(request, 'myapp/register.html', {'form': form})

# def activate(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Your email has been verified successfully. Now you can log in.')
#         return redirect('login')  # Redirect to your login page
#     else:
#         messages.error(request, 'The activation link was invalid, possibly because it has already been used.')
#         return redirect('home')
# # def register(request):
# #     if request.method == 'POST':
# #         form = UserAndResearcherForm(request.POST)
# #         if form.is_valid():
# #             # Try to get the user instance that matches the form's user data
# #             User = get_user_model()
# #             username = form.cleaned_data['username']
# #             email = form.cleaned_data['email']

# #             # Check if this user already exists
# #             if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
# #                 user = User.objects.filter(email=email).first() or User.objects.filter(username=username).first()
# #                 # Now, check if a researcher profile already exists for this user
# #                 if Researcher.objects.filter(user=user).exists():
# #                     messages.error(request, "A researcher profile already exists for this user.")
# #                     return redirect('register')
# #                 else:
# #                     # If the user exists but no researcher profile, create the researcher profile
# #                     form.save(commit=False)
# #                     researcher = Researcher(user=user)
# #                     # Set other researcher fields from form
# #                     researcher.save()
# #                     messages.success(request, 'Researcher profile created successfully.')
# #                     return redirect('home')
# #             else:
# #                 # If user does not exist, create both user and researcher profiles
# #                 user = form.save()  # This should handle both User and Researcher creation
# #                 messages.success(request, 'User and researcher profile created successfully.')
# #                 return redirect('home')
# #     else:
# #         form = UserAndResearcherForm()
# #     return render(request, 'myapp/register.html', {'form': form})
# # views.py
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import ResearchItemForm
# from .models import ResearchItem

# @login_required
# def upload_research_item(request):
#     if request.method == 'POST':
#         form = ResearchItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Submitted successfully.')
#             return redirect('home')
#     else:
#         form = ResearchItemForm(initial={'uploaded_by': request.user.id})
#     return render(request, 'myapp/upload_research_item.html', {'form': form})

# from django.db.models import Q
# def search_research_items(request):
#     query = request.GET.get('q', '')
#     if query:
#         # Search in various fields with OR conditions
#         items = ResearchItem.objects.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(other__icontains=query) |
#             Q(author__icontains=query) |
#             Q(source__icontains=query) |
#             Q(subject__icontains=query) |
#             Q(century__icontains=query) |  # Assuming you want to allow century in query
#             Q(date__icontains=query) |  # Assuming date is stored in a way that makes this query meaningful
#             Q(country__name__icontains=query) |  # For ManyToMany fields like country
#             Q(CE_or_BCE__icontains=query)
#         ).distinct()  # `.distinct()` ensures unique results when querying ManyToMany fields
#     else:
#         items = ResearchItem.objects.all()
#     return render(request, 'myapp/search_results.html', {'items': items, 'query': query})

# # from .forms import ResearchItemSearchForm
# # from django.db.models import Q
# # def search_research_items(request):
# #     form = ResearchItemSearchForm(request.GET)
# #     items = ResearchItem.objects.all()
# #     query = request.GET.get('q', '')

# #     if form.is_valid():
# #         query = form.cleaned_data.get("query")
# #         title = form.cleaned_data.get("title")
# #         century = form.cleaned_data.get("century")
# #         author = form.cleaned_data.get("author")
# #         country = form.cleaned_data.get("country")
# #         CE_or_BCE = form.cleaned_data.get("CE_or_BCE")
# #         if query:
# #             # Search in various fields with OR conditions
# #             items = ResearchItem.objects.filter(
# #                 Q(title__icontains=query) |
# #                 Q(description__icontains=query) |
# #                 Q(other__icontains=query) |
# #                 Q(author__icontains=query) |
# #                 Q(source__icontains=query) |
# #                 Q(subject__icontains=query) |
# #                 Q(century__icontains=query) |  # Assuming you want to allow century in query
# #                 Q(date__icontains=query) |  # Assuming date is stored in a way that makes this query meaningful
# #                 Q(country__name__icontains=query) |  # For ManyToMany fields like country
# #                 Q(CE_or_BCE__icontains=query)
# #             ).distinct()  # `.distinct()` ensures unique results when querying ManyToMany fields
        
# #         if title:
# #             items = items.filter(title__icontains=title)

# #         if century:
# #             items = items.filter(century=century)

# #         if author:
# #             items = items.filter(author__icontains=author)
        
# #         if country:
# #             items = items.filter(country__icontains=country)
        
# #         if CE_or_BCE:
# #             items = items.filter(CE_or_BCE=CE_or_BCE)


# #         else:
# #             items = ResearchItem.objects.all()
# #     return render(request, 'myapp/search_results.html', {'form': form, 'items': items.distinct()})

# # from django.shortcuts import render
# # from django.db.models import Q
# # from .models import ResearchItem
# # from .forms import MultiSearchForm

# # def search_results(request):
# #     form = MultiSearchForm(request.GET or None)
# #     items = ResearchItem.objects.all()

# #     if form.is_valid():
# #         search_by = form.cleaned_data.get("search_by")
# #         query = form.cleaned_data.get("query")

# #         if query:  # Check if a query is provided
# #             q_objects = Q()  # Create an empty Q object to start with
# #             for criteria in search_by:  # Iterate through selected search criteria
# #                 kwargs = {f'{criteria}__icontains': query}
# #                 q_objects |= Q(**kwargs)  # Use | for OR operation
                
# #             items = items.filter(q_objects)  # Apply the constructed Q objects as the filter

# #     return render(request, 'search_results.html', {'form': form, 'items': items})


# from django.shortcuts import get_object_or_404, render

# def research_item_detail(request, pk):
#     research_item = get_object_or_404(ResearchItem, pk=pk)
#     return render(request, 'myapp/research_item_detail.html', {'research_item': research_item})