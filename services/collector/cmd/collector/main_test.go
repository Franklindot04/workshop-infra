package main

import (
	"testing"
)

func TestServerPortPrecedence(t *testing.T) {
	t.Run("COLLECTOR_PORT takes priority", func(t *testing.T) {
		t.Setenv("COLLECTOR_PORT", "9090")
		t.Setenv("PORT", "8080")
		if got := serverPort(); got != "9090" {
			t.Fatalf("expected 9090, got %s", got)
		}
	})

	t.Run("PORT used when COLLECTOR_PORT unset", func(t *testing.T) {
		t.Setenv("COLLECTOR_PORT", "")
		t.Setenv("PORT", "7070")
		if got := serverPort(); got != "7070" {
			t.Fatalf("expected 7070, got %s", got)
		}
	})

	t.Run("default 8080 when both unset", func(t *testing.T) {
		t.Setenv("COLLECTOR_PORT", "")
		t.Setenv("PORT", "")
		if got := serverPort(); got != "8080" {
			t.Fatalf("expected 8080, got %s", got)
		}
	})
}
