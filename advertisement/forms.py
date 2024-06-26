from django import forms
from .models import Advertisement

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['name', 'description', 'terms_condition', 'location',
                  'mobile_number', 'email', 'facebook_link', 'twitter_link', 'instagram_link', 'linkedin_link',
                  'images', 'video']
        labels = {
            'name': 'Company Name',
            'description': 'Advertisement Description',
            'location': 'Advertisement Location',
            'terms_condition': 'Advertisement Terms and Conditions',
            'mobile_number': 'Mobile Number',
            'email': 'Email',
            'facebook_link': 'Facebook Link',
            'twitter_link': 'Twitter Link',
            'instagram_link': 'Instagram Link',
            'linkedin_link': 'LinkedIn Link',
            'images': 'Advertisement Images',
            'video': 'Advertisement Video',
        }
        help_texts = {
            'name': 'Enter the name of your company or brand.',
            'description': 'Provide a brief description of your advertisement.',
            'location': 'Specify the location where the advertisement will be displayed.',
            'terms_condition': 'Add any terms and conditions associated with the advertisement.',
            'mobile_number': 'Enter your contact mobile number.',
            'email': 'Enter your contact email address.',
            'facebook_link': 'Provide the link to your Facebook page or profile.',
            'twitter_link': 'Provide the link to your Twitter account.',
            'instagram_link': 'Provide the link to your Instagram account.',
            'linkedin_link': 'Provide the link to your LinkedIn profile or page.',
            'images': 'Upload images related to your advertisement.',
            'video': 'Upload a video related to your advertisement.',
        }
