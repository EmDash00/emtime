"""A convenient timer package."""

import time


class Timer:
    """A timer which uses `time.perf_counter()` to time events."""

    def __init__(self, interval: float = 1.0, is_paused: bool = False):
        """Create a Timer object.

        Parameters
        ----------
        interval : float
            Interval between timer "ticks" in seconds.

        is_paused : bool
            True to have the timer start paused, False otherwise.

        """
        self._interval = interval
        self._t0 = time.perf_counter()
        self._t_last = time.perf_counter()
        self._t_last_tick = time.perf_counter()

        self._is_paused = is_paused
        self._has_ticked = False
        self._accum_time: float = 0.0

    @property
    def elapsed(self) -> float:
        """Get the elapsed time, in seconds.

        See Also
        --------
        :func:`emtime.Timer.elapsed_ticks()`
        :func:`emtime.Timer.elapsed_ticks_int()`

        """
        if self._is_paused:
            return self._accum_time

        _ = self.tick
        return (time.perf_counter() - self._t0) + self._accum_time

    @property
    def elapsed_ticks_int(self) -> int:
        """Get the whole number of ticks that have elapsed.

        See Also
        --------
        :func:`emtime.Timer.tick_delta()`
        :func:`emtime.Timer.elapsed_ticks()`
        :func:`emtime.Timer.tick()`

        """
        return int(self.elapsed_ticks)

    @property
    def elapsed_ticks(self) -> float:
        """Get the fractional number of ticks that have elapsed.

        See Also
        --------
        :func:`emtime.Timer.elapsed_ticks_int()`
        :func:`emtime.Timer.tick_delta()`
        :func:`emtime.Timer.tick()`

        """
        return self.elapsed / self._interval

    @property
    def tick_delta(self) -> float:
        """Get the time that has passed since the last tick.

        See Also
        --------
        :func:`emtime.Timer.tick()`
        :func:`emtime.Timer.elapsed_ticks()`
        :func:`emtime.Timer.elapsed_ticks_int()`

        """
        tick_delta = time.perf_counter() - self._t_last_tick

        if tick_delta > self._interval:
            self._has_ticked = True
            self._t_last_tick += (
                tick_delta // self._interval
            ) * self._interval

        return time.perf_counter() - self._t_last_tick

    @property
    def tick(self) -> bool:
        """Check if at least one tick has occurred since the last call to this
        function or :func:`emtime.Timer.tick_delta()`.

        See Also
        --------
        :func:`emtime.Timer.elapsed_ticks()`
        :func:`emtime.Timer.elapsed_ticks_int()`
        :func:`emtime.Timer.elapsed_tick_delta()`

        """
        _ = self.tick_delta  # Call property to update tick flag.

        if self._has_ticked:
            self._has_ticked = False
            return True

        return False

    @property
    def delta(self) -> float:
        """Get the time that elapsed since the last call to this function.

        See Also
        --------
        :func:`emtime.Timer.tick_delta()`

        """
        t = time.perf_counter()
        dt = t - self._t_last
        self._t_last = t
        return dt

    def reset(self):
        """Reset the timer to 0 elapsed time."""
        self._t0 = time.perf_counter()

    def pause(self):
        """Pause the timer so that calls to `Timer.elapsed` do not change.

        See Also
        --------
        :func:`emtime.Timer.resume()`

        """
        # Save current time.
        self._accum_time += self.elapsed

        self._is_paused = True

    def resume(self):
        """Resumes the timer.

        See Also
        --------
        :func:`emtime.Timer.pause()`

        """
        # Save current time.
        self._is_paused = False
        self._t0 = time.perf_counter()

        self.reset()
