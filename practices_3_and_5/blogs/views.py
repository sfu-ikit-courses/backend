from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Post


class BlogListView(ListView):
    model = Post
    # queryset = Post.objects.order_by('id')
    paginate_by = 2
    template_name = "post/post_list.html"


class BlogDetailView(DetailView):
    model = Post
    template_name = "post/post_detail.html"


class BlogCreateView(SuccessMessageMixin, CreateView):
    model = Post
    template_name = "post/post_new.html"
    fields = ["name", "description", "featured_image"]
    success_message = "%(name)s успешно создан"

    # success_url = reverse_lazy("post_list")
    # def get_success_url(self):
    #     return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    # def form_valid(self, form):
    #     name = form.cleaned_data['name']
    #     if name == "500":
    #         form.add_error('name', "Сообщение")
    #         messages.error(self.request, "В данный момент у вас не хватает полномочий")
    #         return self.form_invalid(form)
    #
    #     messages.success(self.request, f"{name} успешно создан")
    #     return super().form_valid(form)
    #
    # def form_invalid(self, form):
    #     messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
    #     return super().form_invalid(form)


class BlogUpdateView(SuccessMessageMixin, UpdateView):
    model = Post
    template_name = "post/post_edit.html"
    # success_url = reverse_lazy("post_list")
    fields = ["name", "description", "featured_image"]
    success_message = "%(name)s успешно обновлен"


class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post/post_delete.html"
    success_url = reverse_lazy("post_list")
