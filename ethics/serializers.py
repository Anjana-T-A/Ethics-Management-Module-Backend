from rest_framework import serializers
from .models import EthicsForm

class EthicsFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EthicsForm
        fields = "__all__"

    def validate_human_participants(self, value):
        expected_keys = {"vulnerable_persons", "under_18", "patients", "staff"}
        if not isinstance(value, dict):
            raise serializers.ValidationError("Invalid format. Expected a JSON object.")
        if set(value.keys()) != expected_keys:
            raise serializers.ValidationError(f"Missing or extra fields. Expected {expected_keys}.")
        if not all(isinstance(v, bool) for v in value.values()):
            raise serializers.ValidationError("All values must be boolean (true/false).")
        return value

    def validate_subject_matter(self, value):
        expected_keys = {"sensitive_issues", "illegal_activities", "self_respect_risk"}
        if not isinstance(value, dict):
            raise serializers.ValidationError("Invalid format. Expected a JSON object.")
        if set(value.keys()) != expected_keys:
            raise serializers.ValidationError(f"Missing or extra fields. Expected {expected_keys}.")
        if not all(isinstance(v, bool) for v in value.values()):
            raise serializers.ValidationError("All values must be boolean (true/false).")
        return value
