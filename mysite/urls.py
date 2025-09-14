from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from npc_api import views

schema_view = get_schema_view(
    openapi.Info(
        title="NPC Generator API",
        default_version='v1',
        description="API for generating NPC characters based on stories",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('npc_api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # frontend views
    path('', views.main_page, name='main'),
    path('world/', views.world_page, name='world'),
    path('characters/', views.characters_page, name='characters'),
    path('conversation/', views.conversation_page, name='conversation'),
    path('conversations/<int:character_id>/history/', views.ConversationHistoryTemplateView.as_view(), name='conversation-history-html'),
    path('quick-add-fantasy/', views.quick_add_fantasy, name='quick-add-fantasy'),
    path('about/', views.about_page, name='about'),
]
