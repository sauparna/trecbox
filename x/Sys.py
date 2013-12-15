
import os, subprocess, sys

class Sys():
    def __init__(self, env, doc, topic, model, qrel):
        self.env = env
        self.doc = doc
        self.topic = topic
        self.qrel = qrel
        self.model = model
