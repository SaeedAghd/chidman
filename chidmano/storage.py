from whitenoise.storage import CompressedManifestStaticFilesStorage


class SafeCompressedManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """
    Wrapper around Whitenoise's CompressedManifestStaticFilesStorage that
    falls back to the original filename when the manifest entry is missing.
    This prevents ValueError: Missing staticfiles manifest entry errors at runtime
    if the manifest is not present or missing some keys.
    """

    def stored_name(self, name):
        try:
            return super().stored_name(name)
        except ValueError:
            # Fall back to the un-hashed name so templates don't raise 500.
            return name


