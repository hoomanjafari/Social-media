from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.utils.text import slugify
from .forms import UserProfileEdit, UserPostCreateForm, PostCommentCreateForm, CommentReplayForm
from .models import UserPost
from Home.models import FollowUser, PostLike


class UserProfileDetail(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        post = UserPost.objects.filter(user=user)
        followed = FollowUser.objects.filter(user_is_follow=request.user.id, user_is_followed=user)
        is_follow = False
        if followed.exists():
            is_follow = True
        return render(request, 'accounts/profile.html', {'user': user, 'post': post, 'is_follow': is_follow})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserProfileEdit(instance=request.user.profile_related, initial={'email': request.user.email})
        return render(request, 'accounts/edit_profile.html', {'form': form})

    def post(self, request):
        x = UserProfileEdit(self.request.POST, instance=request.user.profile_related)
        if x.is_valid():
            edited = x.save(commit=False)
            edited.user = request.user
            x.save()
            request.user.email = x.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Edit done !', 'success')
            return redirect('accounts:profile', request.user.id)
        else:
            return render(request, 'accounts/edit_profile.html', {'form': x})


class PasswordResetView(auth_views.PasswordResetView):

    template_name = 'accounts/reset_password_email/password_reset_form.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'accounts/reset_password_email/password_reset_email.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/reset_password_email/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/reset_password_email/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/reset_password_email/password_reset_complete.html'


class UserPostCreateView(LoginRequiredMixin, View):
    form_class = UserPostCreateForm

    def get(self, request, **kwargs):
        return render(request, 'accounts/user_post.html', {'form': self.form_class})

    def post(self, request, **kwargs):
        x = self.form_class(self.request.POST)
        if x.is_valid():
            post = x.save(commit=False)
            post.user = request.user
            post.slug = slugify(x.cleaned_data['body'][:16])
            x.save()
            messages.success(request, 'Your post has been sent !', 'success')
            return redirect('home:home')


class UserPostEditView(LoginRequiredMixin, View):
    form_class = UserPostCreateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(UserPost, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, **kwargs):
        form = self.form_class(instance=self.post_instance)
        return render(request, 'accounts/edit_user_post.html', {'form': form})

    def post(self, request, **kwargs):
        x = self.form_class(self.request.POST, instance=self.post_instance)
        if x.is_valid():
            edited = x.save(commit=False)
            edited.slug = slugify(x.cleaned_data['body'[:10]])
            x.save()
            messages.success(request, 'Post is edited ...', 'success')
            return redirect('accounts:profile', request.user.id)


class UserPostDeleteView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(UserPost, pk=kwargs['post_id'])
        if request.user.id == user.user.id:
            user.delete()
            messages.success(request, 'Post has been Deleted ...', 'danger')
            return redirect('accounts:profile', user.user.id)
        else:
            messages.error(request, 'You are not this post owner !!!', 'danger')
            return redirect('home:home')


class PostDetailView(View):

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(UserPost, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, **kwargs):
        post = self.post_instance
        comment_form = PostCommentCreateForm
        comment = post.post_comment_related.filter(is_replay=False)
        replay = CommentReplayForm
        liked = PostLike.objects.filter(user_liked=request.user.id, post_liked=post)
        is_like = False
        if liked.exists():
            is_like = True
        return render(request, 'accounts/post_detail.html', {
            'post': post, 'comment_form': comment_form, 'comment': comment, 'replay': replay, 'is_like': is_like
        })

    def post(self, request, **kwargs):
        x = PostCommentCreateForm(self.request.POST)
        post = self.post_instance
        if x.is_valid():
            comment = x.save(commit=False)
            comment.user = request.user
            comment.post = post
            x.save()
            messages.success(request, 'Your comment has been sent ...', 'success')
            return redirect('accounts:post_detail', post.id, post.slug)


class CommentReplayView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        x = CommentReplayForm(self.request.POST)
        post = get_object_or_404(UserPost, pk=kwargs['post_id'])
        if x.is_valid():
            replay = x.save(commit=False)
            replay.is_replay = True
            replay.user = request.user
            replay.post = post
            x.save()
            messages.success(request, 'Replay sent...', 'success')
            return redirect('accounts:post_detail', post.id, post.slug)
