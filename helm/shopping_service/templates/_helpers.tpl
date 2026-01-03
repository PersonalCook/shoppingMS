{{- define "shopping_service.name" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- $name | lower | replace "_" "-" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "shopping_service.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | lower | replace "_" "-" | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := include "shopping_service.name" . -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | lower | replace "_" "-" | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | lower | replace "_" "-" | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "shopping_service.labels" -}}
app.kubernetes.io/name: {{ include "shopping_service.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "shopping_service.selectorLabels" -}}
app.kubernetes.io/name: {{ include "shopping_service.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
