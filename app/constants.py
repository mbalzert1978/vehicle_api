from dataclasses import dataclass
from enum import StrEnum
from typing import Final

# Database naming convention constants
DB_NAMING_CONVENTION: Final[dict[str, str]] = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Environment(StrEnum):
    """Enumeration of application environments."""

    LOCAL = "LOCAL"
    TESTING = "TESTING"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self) -> bool:
        """Check if the environment is a debug environment.

        Returns:
            True if the environment allows debugging features.
        """
        assert isinstance(self, Environment), "Self must be an Environment instance"

        return self in {self.LOCAL, self.STAGING, self.TESTING}

    @property
    def is_testing(self) -> bool:
        """Check if the environment is the testing environment.

        Returns:
            True if this is the testing environment.
        """
        assert isinstance(self, Environment), "Self must be an Environment instance"

        return self is self.TESTING

    @property
    def is_deployed(self) -> bool:
        """Check if the environment is a deployed environment.

        Returns:
            True if the environment is staging or production.
        """
        assert isinstance(self, Environment), "Self must be an Environment instance"

        return self in {self.STAGING, self.PRODUCTION}


@dataclass(frozen=True, slots=True)
class EnvironmentConfig:
    """Configuration for environment-specific settings."""

    environment: Environment

    @property
    def allows_debugging(self) -> bool:
        """Check if debugging is allowed in this environment.

        Returns:
            True if debugging features should be enabled.
        """
        assert isinstance(self.environment, Environment), (
            "Environment must be an Environment instance"
        )

        return self.environment.is_debug

    @property
    def requires_security(self) -> bool:
        """Check if enhanced security measures are required.

        Returns:
            True if this environment requires production-level security.
        """
        assert isinstance(self.environment, Environment), (
            "Environment must be an Environment instance"
        )

        return self.environment.is_deployed


class EnvironmentConfigFactory:
    """Factory for creating environment configuration instances."""

    @staticmethod
    def new(environment: Environment) -> EnvironmentConfig:
        """Create a new environment configuration.

        Args:
            environment: The environment to create configuration for.

        Returns:
            A new EnvironmentConfig instance.
        """
        assert isinstance(environment, Environment), "Environment must be an Environment instance"

        result = EnvironmentConfig(environment=environment)

        assert isinstance(result, EnvironmentConfig), "Result must be an EnvironmentConfig instance"
        assert result.environment == environment, "Environment must be preserved"

        return result

    @staticmethod
    def new_local() -> EnvironmentConfig:
        """Create configuration for local environment.

        Returns:
            EnvironmentConfig configured for local development.
        """
        result = EnvironmentConfigFactory.new(Environment.LOCAL)

        assert isinstance(result, EnvironmentConfig), "Result must be an EnvironmentConfig instance"
        assert result.environment == Environment.LOCAL, "Must be local environment"

        return result

    @staticmethod
    def new_testing() -> EnvironmentConfig:
        """Create configuration for testing environment.

        Returns:
            EnvironmentConfig configured for testing.
        """
        result = EnvironmentConfigFactory.new(Environment.TESTING)

        assert isinstance(result, EnvironmentConfig), "Result must be an EnvironmentConfig instance"
        assert result.environment == Environment.TESTING, "Must be testing environment"

        return result

    @staticmethod
    def new_staging() -> EnvironmentConfig:
        """Create configuration for staging environment.

        Returns:
            EnvironmentConfig configured for staging.
        """
        result = EnvironmentConfigFactory.new(Environment.STAGING)

        assert isinstance(result, EnvironmentConfig), "Result must be an EnvironmentConfig instance"
        assert result.environment == Environment.STAGING, "Must be staging environment"

        return result

    @staticmethod
    def new_production() -> EnvironmentConfig:
        """Create configuration for production environment.

        Returns:
            EnvironmentConfig configured for production.
        """
        result = EnvironmentConfigFactory.new(Environment.PRODUCTION)

        assert isinstance(result, EnvironmentConfig), "Result must be an EnvironmentConfig instance"
        assert result.environment == Environment.PRODUCTION, "Must be production environment"

        return result
