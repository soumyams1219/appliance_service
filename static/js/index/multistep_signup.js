/* Code to validate booking form */
const steps = document.querySelectorAll('.step');
const nextBtns = document.querySelectorAll('.next-step');
const prevBtns = document.querySelectorAll('.prev-step');
const form = document.getElementById('multiStepForm');

let currentStep = 0;

function showStep(index) {
  steps.forEach((step, i) => {
    step.classList.toggle('d-none', i !== index);
  });
}

function validateCurrentStep() {
  const currentInputs = steps[currentStep].querySelectorAll('input, select');
  for (let input of currentInputs) {
    if (!input.checkValidity()) {
      input.reportValidity();
      return false;
    }
  }
  return true;
}

nextBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    if (validateCurrentStep()) {
      currentStep++;
      showStep(currentStep);
    }
  });
});

prevBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    currentStep--;
    showStep(currentStep);
  });
});

form.addEventListener('submit', e => {
  if (!validateCurrentStep()) {
    e.preventDefault(); // Stop submission only if validation fails
    return;
  }
  // Allow form to submit to Django normally
});


// Initial step display
showStep(currentStep);