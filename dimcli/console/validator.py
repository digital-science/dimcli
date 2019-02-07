#!/usr/bin/python
# -*- coding: utf-8 -*-

from prompt_toolkit.validation import Validator, ValidationError

#
# VALIDATOR
#
#
# UNUSED FOR NOW


class BasicValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and "return" not in text:

            raise ValidationError(
                message="A query must include a return statement",
                # cursor_position=i
            )
