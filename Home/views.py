from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, LoginUserForm, UserSearchBox, PostSearchBox
from .models import FollowUser, PostLike, UserPost


class Home(LoginRequiredMixin, View):
    def get(self, request):
        search_user = UserSearchBox
        founded_user = ''
        if self.request.GET.get('search_user'):
            founded_user = User.objects.filter(username__contains=self.request.GET['search_user'])
        search_post = PostSearchBox
        posts = UserPost.objects.order_by('-created')
        if self.request.GET.get('post_search'):
            posts = posts.filter(body__contains=request.GET['post_search'])
        return render(request, 'home/index.html', {
            'search_user': search_user, 'founded_user': founded_user, 'posts': posts, 'search_post': search_post
        })


class RegisterUserView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You can not register when you are login !!!', 'danger')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = RegisterForm()
        return render(request, 'home/register.html', {'form': form})

    def post(self, request):
        x = RegisterForm(self.request.POST)
        if x.is_valid():
            cd = x.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            messages.success(request, 'You are successfully registered !', 'success')
            return redirect('home:home')
        else:
            return render(request, 'home/register.html', {'form': x})


class LoginUserView(View):
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next', None)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You can not login agine when you are already logged in !!!', 'danger')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = LoginUserForm()
        return render(request, 'home/login.html', {'form': form})

    def post(self, request):
        x = LoginUserForm(self.request.POST)
        if x.is_valid():
            cd = x.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You have logged in ...', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                messages.error(request, 'Username or Password is incorrect !!', 'danger')
                return redirect('home:login')


class LogoutUserView(LoginRequiredMixin, View):
    # login_url = '/Home/login/'

    def get(self, request):
        logout(request)
        messages.success(request, 'You have logged out ...', 'success')
        return redirect('home:login')


class FollowUserView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        user_followed = FollowUser.objects.filter(user_is_follow=request.user, user_is_followed=user)
        if user_followed.exists():
            user_followed.delete()
            messages.success(request, 'You unfollow this user...', 'danger')
            return redirect('accounts:profile', user.id)
        elif not user_followed.exists():
            if request.user.id != user.id:
                FollowUser.objects.create(user_is_follow=request.user, user_is_followed=user)
                messages.success(request, 'You Follow this user ...', 'success')
                return redirect('accounts:profile', user.id)
            else:
                messages.error(request, 'You can not follow your self !!!', 'danger')
                return redirect('accounts:profile', request.user.id)


class LikePostView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        post = get_object_or_404(UserPost, pk=kwargs['post_id'])
        liked = PostLike.objects.filter(user_liked=request.user, post_liked=post)
        if liked.exists():
            liked.delete()
            messages.success(request, 'You UNLIKE this post ...', 'danger')
            return redirect('accounts:post_detail', post.id, post.slug)
        elif not liked.exists():
            PostLike.objects.create(user_liked=request.user, post_liked=post)
            messages.success(request, 'You LIKE this post ...', 'success')
            return redirect('accounts:post_detail', post.id, post.slug)
