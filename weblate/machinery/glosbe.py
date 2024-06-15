# Copyright © Michal Čihař <michal@weblate.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .base import DownloadTranslations, MachineTranslation


class GlosbeTranslation(MachineTranslation):
    """Glosbe machine translation support."""

    name = "Glosbe"
    max_score = 90
    do_cleanup = False

    def map_language_code(self, code):
        """Convert language to service specific code."""
        return super().map_language_code(code).replace("_", "-").split("-")[0].lower()

    def is_supported(self, source_language, target_language) -> bool:
        """Any language is supported."""
        return True

    def download_translations(
        self,
        source_language,
        target_language,
        text: str,
        unit,
        user,
        threshold: int = 75,
    ) -> DownloadTranslations:
        """Download list of possible translations from a service."""
        response = self.request(
            "post",
            "https://translator-api.glosbe.com/translateByLangWithScore",
            params={"sourceLang": source_language, "targetLang": target_language},
            data=text,
            headers={"Content-Type": "text/plain"},
        )
        payload = response.json()

        if "translation" not in payload or payload["translation"] is None:
            return
        yield {
            "text": payload["translation"],
            "quality": self.max_score,
            "service": self.name,
            "source": text,
        }
