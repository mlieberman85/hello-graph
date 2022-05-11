package main

import (
	"github.com/mlieberman85/hello-graph/schema"
	"time"
)

schema.#Provenance & {
	"_type": "https://in-toto.io/Statement/v0.1"
	subject: [
		_drv.outputs,
	]

	// Predicate:
	predicateType: "https://slsa.dev/provenance/v0.2"
	predicate: {
		builder: {
			id: schema.#TypeURI & "file://\(_drv.builder)"
		}
		buildType: schema.#TypeURI & "https://nixos.org/build/0.1"
		invocation: {
			configSource?: {// TBD
				uri?:        schema.#ResourceURI
				digest?:     schema.#DigestSet
				entryPoint?: string
			}
			parameters: {
				"args": _drv.args
			}
			environment: {
				_drv.env
			}
		}
		buildConfig?: {...}
		metadata?: {
			buildInvocationId?: string
			buildStartedOn?:    time.Time
			buildFinishedOn?:   time.Time
			completeness?: {
				parameters?:  bool
				environment?: bool
				materials?:   bool
			}
			reproducible?: bool
		}
		materials: _drv.inputs
	}
}
